import datetime
import time
import numpy as np
import pandas as pd
import requests
import functools
from typing import List
from credentials import DATA_DIRECTORY


def try_ping_google(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        i = 60
        while i >= 1:
            try:
                url = "https://google.com"
                response = requests.get(url)
            except:
                time.sleep(i)
                if i > 360:
                    raise Exception
                i += 60
            break
        ret = method(self, *args, **kwargs)
        return ret

    return wrapper


class CustomReport:
    def __init__(self,
                report_name: str,
                project_name: str = "ED",
                report_type: str = "default"):
        self.at_report_name: str = report_name
        self.at_project_name: str = project_name
        self.at_report_type: str = report_type
        self.at_file_name: str = None
        dt_today = datetime.date.today()
        dt_yesterday = str(dt_today - datetime.timedelta(days=1))
        self.at_start_date: str = dt_yesterday
        self.at_end_date: str = dt_yesterday
        self.at_report_df = pd.DataFrame()


    def create_file_name(self):
        self.at_file_name = f"{self.at_project_name}_{self.at_report_type}_{self.at_report_name}"
        return self.at_file_name
    
    def overwriting_old_csv_report(self, df=pd.DataFrame(), file_name: str = None, drop_duplicates: bool = False, duplicates: List[str] = None):
        '''If the method is called without arguments, the values ​​from the attributes will be used.

        '''
        if df.empty == True:
            df = self.at_report_df
        if file_name is None:
            self.create_file_name()
            file_name = self.at_file_name
        file_path = f"{DATA_DIRECTORY}{file_name}.csv"
        try:
            old_df = pd.read_csv(file_path)
        except:
            df.to_csv(file_path, index=False)
        else:
            df = pd.concat([old_df, df])
            if drop_duplicates == True:
                df = df.drop_duplicates(subset=duplicates)
            df.to_csv(file_path, index=False)
        print("Report exported to csv")
        return df


    
    def collect_test(method):
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