import numpy as np
import pandas as pd
from typing import List
import datetime
import functools
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (DateRange, Dimension, Filter,
                                                FilterExpression, Metric,
                                                OrderBy, RunReportRequest,
                                                CohortSpec, GetMetadataRequest,
                                                MetricType,
                                                FilterExpressionList)

from custom_reports.modules.class_report import CustomReport

from google_apis.cred.credentials import (GA4_ED_PROPERTY_ID, GA4_EM_PROPERTY_ID,
                                          GOOGLE_CREDENTIALS_JSON_PATH)
from google_apis.data_api.config.default_configuration import *


class GA4Exception(Exception):
    """base class for GA4 exceptions"""


class GA4Report(CustomReport):
    """
    """

    def __init__(self,
                 report_name: str,
                 project_name: str = "ED",
                 report_type: str = "default"):
        CustomReport.__init__(self, report_name, project_name, report_type)
        #
        self.at_ga4_dim_list: List[str] = None
        self.at_ga4_metr_list: List[str] = None
        #
        self.at_limit: int = 100000
        self.at_offset: int = 0
        self.at_filter: str = None
        self.at_ga4_response = None
        self.at_all_respons_rows: int = None
        self.at_taken_rows_count: int = None
        self.at_tokens_per_day_total: int = None
        self.at_tokens_per_hour_total: int = None
        self.at_quota_df = pd.DataFrame()
        self.__set_report_source()

    def __set_report_source(self):
        self.at_credentials_json_path: str = GOOGLE_CREDENTIALS_JSON_PATH
        if self.at_project_name == "ED":
            self.at_property_id: str = GA4_ED_PROPERTY_ID
        elif self.at_project_name == "EM":
            self.at_property_id: str = GA4_EM_PROPERTY_ID
        else:
            raise ValueError("Invalid project name")
        
    def set_filter(self, filter_name: str):
        """Доступно 3 фильтра:\n
        'card'\n
        'search_term'\n
        'email'\n
        """
        if filter_name == 'card':
            self.at_filter = self.card_dim_filter()
        elif filter_name == 'search_term':
            self.at_filter = self.search_dim_filter()
        elif filter_name == 'email':
            self.at_filter = self.email_dim_filter()
        else:
            raise ValueError('Invalid filter name')

    def collect_quota(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            self.create_file_name()
            print("dimension_list - ", self.at_ga4_dim_list)
            print("metric_list - ", self.at_ga4_metr_list)
            ret = method(self, *args, **kwargs)
            self.ga4_response_to_df()
            self.ga4_report_quota_to_df()
            self.ga4_overwriting_old_quota_excel()
            print(self.at_all_respons_rows,
                  self.at_taken_rows_count + self.at_offset,
                  self.at_tokens_per_day_total, self.at_tokens_per_hour_total)
            return ret

        return wrapper

    def card_dim_filter(self):
        filter = FilterExpression(and_group=FilterExpressionList(expressions=[
            FilterExpression(filter=Filter(
                field_name=card_field_name,
                string_filter=Filter.StringFilter(
                    value=card_filters_value,
                    match_type=Filter.StringFilter.MatchType.FULL_REGEXP,
                ))),
            # FilterExpression(filter=Filter(
            #     field_name="unifiedPageScreen",
            #     string_filter=Filter.StringFilter(value="(.*categ.*)|(/)",
            #     match_type=Filter.StringFilter.MatchType.FULL_REGEXP,)
            # ))
        ]))
        return filter
    
    def search_dim_filter(self):
        filter = FilterExpression(and_group=FilterExpressionList(expressions=[
            FilterExpression(filter=Filter(
                field_name=search_field_name,
                string_filter=Filter.StringFilter(
                    value=search_filters_value,
                    match_type=Filter.StringFilter.MatchType.FULL_REGEXP,
                ))),
            # FilterExpression(filter=Filter(
            #     field_name="unifiedPageScreen",
            #     string_filter=Filter.StringFilter(value="(.*categ.*)|(/)",
            #     match_type=Filter.StringFilter.MatchType.FULL_REGEXP,)
            # ))
        ]))
        return filter

    def email_dim_filter(self):
        filter = FilterExpression(and_group=FilterExpressionList(expressions=[
            FilterExpression(filter=Filter(
                field_name=email_field_name,
                string_filter=Filter.StringFilter(
                    value=email_filters_value,
                    match_type=Filter.StringFilter.MatchType.FULL_REGEXP,
                ))),
            # FilterExpression(filter=Filter(
            #     field_name="unifiedPageScreen",
            #     string_filter=Filter.StringFilter(value="(.*categ.*)|(/)",
            #     match_type=Filter.StringFilter.MatchType.FULL_REGEXP,)
            # ))
        ]))
        return filter


    @collect_quota
    def ga4_run_metadata_report_to_df(self):
        """Runs a metadata report on a Google Analytics 4 property"""
        try:
            client = BetaAnalyticsDataClient(
                client_options={
                    "credentials_file": self.at_credentials_json_path
                })
            request = GetMetadataRequest(
                name=f"properties/{self.at_property_id}/metadata")
            response = client.get_metadata(request)
            output = []
            for dimension in response.dimensions:
                output.append({
                    "API_Name": f"{dimension.api_name}",
                    "UI_Name": f"{dimension.ui_name}",
                    "Custom_definition": f"{dimension.custom_definition}",
                    "Metric_type": "N/A"
                })
            for metric in response.metrics:
                output.append({
                    "API_Name": f"{metric.api_name}",
                    "UI_Name": f"{metric.ui_name}",
                    "Custom_definition": f"{metric.custom_definition}",
                    "Metric_type": f"{MetricType(metric.type_).name}"
                })
            df = pd.DataFrame(output)
            # setting class attributes
            self.at_report_df = df
            print("metadata report completed")
            return df
        except IOError as e:
            raise GA4Exception(e)
        

    @collect_quota
    def ga4_run_report_request(self,
                               limit_int: int = None,
                               offset_int: int = None,
                               start_date_str: str = None,
                               end_date_str: str = None,
                               dimension_list: List[str] = None,
                               metric_list: List[str] = None):
        # if the method was called without arguments, then the values from the attributes are used
        if limit_int == None:
            limit_int = self.at_limit
        if offset_int == None:
            offset_int = self.at_offset
        if start_date_str == None:
            start_date_str = f"{self.at_start_date}"
        if end_date_str == None:
            end_date_str = f"{self.at_end_date}"
        if dimension_list == None:
            dimension_list = self.at_ga4_dim_list
        if metric_list == None:
            metric_list = self.at_ga4_metr_list

        try:
            client = BetaAnalyticsDataClient(
                client_options={
                    "credentials_file": self.at_credentials_json_path
                })
            request = RunReportRequest(
                property=f"properties/{self.at_property_id}",
                dimensions=[Dimension(name=dim) for dim in dimension_list],
                metrics=[Metric(name=met) for met in metric_list],
                date_ranges=[
                    DateRange(start_date=start_date_str, end_date=end_date_str)
                ],
                dimension_filter=self.at_filter,
                limit=limit_int,
                offset=offset_int,
                return_property_quota=True)
            response = client.run_report(request)
            # counting the actual number of rows received in the report
            taken_rows_count = 0
            for row in response.rows:
                taken_rows_count += 1
            # setting class attributes
            self.at_taken_rows_count = taken_rows_count
            self.at_ga4_response = response
            print("ga4_run_report_request - successful")
            return response, taken_rows_count, offset_int
        # except Exception as e:
        #     raise GA4Exception(e)
        except Exception as e:
            raise e

    def ga4_response_to_df(self, response=None):
        # if the method was called without arguments, then the values from the attributes are used
        if response == None:
            response = self.at_ga4_response

        headers = [header.name for header in response.dimension_headers
                   ] + [header.name for header in response.metric_headers]
        rows = []
        for row in response.rows:
            rows.append(
                [dimension_value.value for dimension_value in row.dimension_values] +
                [metric_value.value for metric_value in row.metric_values])
        ga4_new_pd_report_df = pd.DataFrame(rows, columns=headers)
        all_respons_rows = response.row_count
        # setting class attributes
        self.at_report_df = ga4_new_pd_report_df
        self.at_all_respons_rows = all_respons_rows
        print("ga4_response_to_df - successful")
        return ga4_new_pd_report_df, all_respons_rows

    def ga4_report_quota_to_df(self,
                               ga4_response=None,
                               taken_rows_count=None,
                               offset_int=None):
        # if the method was called without arguments, then the values from the attributes are used
        file_name = self.at_file_name
        if ga4_response == None:
            ga4_response = self.at_ga4_response
        if taken_rows_count == None:
            taken_rows_count = self.at_taken_rows_count
        if offset_int == None:
            offset_int = self.at_offset

        try:
            if "property_quota" in ga4_response:
                headers = [
                    "date_time",
                    "file_name",
                    "all_rows_count_in_report",
                    "rows_in_last_report",
                    "report_offset",
                    "tokens_per_day",
                    "con_tokens_per_day",
                    "tokens_per_hour",
                    "con_tokens_per_hour",
                    "concurrent_requests",
                    "server_errors_per_project_per_hour",
                    "potentially_thresholded_requests_per_hour",
                ]
                rows = []
                dt = str(datetime.datetime.now())
                rows.append([
                    dt,
                    file_name,
                    ga4_response.row_count,
                    taken_rows_count,
                    offset_int,
                    ga4_response.property_quota.tokens_per_day.remaining,
                    ga4_response.property_quota.tokens_per_day.consumed,
                    ga4_response.property_quota.tokens_per_hour.remaining,
                    ga4_response.property_quota.tokens_per_hour.consumed,
                    ga4_response.property_quota.concurrent_requests.remaining,
                    ga4_response.property_quota.
                    server_errors_per_project_per_hour.remaining,
                    ga4_response.property_quota.
                    potentially_thresholded_requests_per_hour.remaining,
                ])
                ga4_new_pd_quota_table = pd.DataFrame(rows, columns=headers)
                self.at_quota_df = ga4_new_pd_quota_table
                self.at_tokens_per_day_total = ga4_response.property_quota.tokens_per_day.remaining
                self.at_tokens_per_hour_total = ga4_response.property_quota.tokens_per_hour.remaining
                print("ga4_report_quota_to_df - successful")
        except:
            raise "unable to add quota information to DF"
        return ga4_new_pd_quota_table

    def ga4_overwriting_old_quota_excel(self,
                                        ga4_new_pd_quota_table=pd.DataFrame()):
        # if the method was called without arguments, then the values from the attributes are used
        if ga4_new_pd_quota_table.empty == True:
            ga4_new_pd_quota_table = self.at_quota_df

        try:
            ga4_old_pd_quota_table = pd.read_excel("ga4_pd_quota_table.xlsx")
            ga4_new_pd_quota_table = pd.concat(
                [ga4_old_pd_quota_table, ga4_new_pd_quota_table])
            ga4_new_pd_quota_table.to_excel("ga4_pd_quota_table.xlsx",
                                            index=False)
        except:
            ga4_new_pd_quota_table.to_excel("ga4_pd_quota_table.xlsx",
                                            index=False)
        print("successful add quota information to excel")

    @CustomReport.try_ping_google
    def ga4_all_rows_to_df(self):
        self.ga4_run_report_request()
        while self.at_taken_rows_count + self.at_offset < self.at_all_respons_rows:
            if self.at_all_respons_rows - (self.at_taken_rows_count +
                                           self.at_offset) > 100000:
                self.at_limit = 100000
            else:
                self.at_limit = self.at_all_respons_rows - (
                    self.at_taken_rows_count + self.at_offset)
            self.at_offset += self.at_taken_rows_count
            report_df = self.at_report_df
            self.ga4_run_report_request()
            self.at_report_df = pd.concat([report_df, self.at_report_df])
        return self.at_report_df


# if __name__ == '__main__':
