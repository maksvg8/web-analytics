import pandas as pd
import requests
from typing import List
import datetime
import functools

from custom_reports.modules.class_report import CustomReport, try_ping_google

from yandex_apis.cred.credentials import (
    YM_TOKEN,
    YM_CLIENT_ID,
    YM_ED_COUNTER_ID,
    YM_EM_COUNTER_ID,
    YM_JB_COUNTER_ID
)

from yandex_apis.ym_reporting_api.config.default_configuration import *


class YandexMetricReport(CustomReport):
    """ 
    report typs: "default", "campaign_report", "kufar_report", "edadeal_report", "banner_report", "category_report"

    """

    def __init__(
        self, report_name: str, project_name: str = 'ED', report_type: str = "default"
    ):
        CustomReport.__init__(self, report_name, project_name, report_type)
        self.ym_token: str = YM_TOKEN
        self.ym_client_id: str = YM_CLIENT_ID
        #
        self.at_ym_dim: str = ""
        self.at_ym_metr: str = ""
        #
        self.at_limit: int = 100000
        self.at_offset: int = 1
        self.at_filters: str = ""
        self.at_ym_response = None
        self.at_ym_data = None
        self.at_report_df = pd.DataFrame()
        self.at_total_rows: int = None
        self.__set_report_source()
        self.__check_report_type()

    def __set_report_source(self):
        if self.at_project_name == 'ED':
            self.ym_counter_id = YM_ED_COUNTER_ID
        elif self.at_project_name == 'EM':
            self.ym_counter_id = YM_EM_COUNTER_ID
        elif self.at_project_name == 'JB':
            self.ym_counter_id = YM_JB_COUNTER_ID
        else:
            raise ValueError("Invalid project name")

    def __check_report_type(self):
        if self.at_report_type == "default":
            ...
        elif self.at_report_type == "campaign_report":
            self.__set_campaign_report_params()
        elif self.at_report_type == "kufar_report":
            self.__set_kufar_report_params()
        elif self.at_report_type == "edadeal_report":
            self.__set_edadeal_report_params()
        elif self.at_report_type == "banner_report":
            self.__set_banner_report_params()
        elif self.at_report_type == "category_report":
            self.__set_category_report_params()

    def __set_campaign_report_params(self):
        self.at_ym_dim = DIM_CAMPAIGN_REPORT
        self.at_ym_metr = METR_CAMPAIGN_REPORT
        if self.at_project_name == 'ED':
            self.at_ym_metr += ',' + METR_ED_REGISTRATION
            self.at_filters = FILTER_ED_CAMPAIGN
            ...
        elif self.at_project_name == 'EM':
            self.at_ym_metr += ',' + METR_EM_REGISTRATION
            self.at_filters = FILTER_EM_CAMPAIGN
            ...
        elif self.at_project_name == 'JB':
            self.at_ym_metr = METR_CAMPAIGN_JB_REPORT + ',' + METR_JB_FORM
            self.at_filters = FILTER_JB_CAMPAIGN
            ...
        else:
            raise ValueError("Invalid project name")

    def __set_kufar_report_params(self):
        self.at_ym_dim = DIM_KUFAR_REPORT
        self.at_ym_metr = METR_KUFAR_REPORT
        if self.at_project_name == 'EM':
            self.at_ym_metr += ',' + METR_EM_REGISTRATION
            self.at_filters = FILTER_EM_KUFAR
            ...
        else:
            raise ValueError("Invalid project name")

    def __set_edadeal_report_params(self):
        self.at_ym_dim = DIM_EDADEAL_REPORT
        self.at_ym_metr = METR_EDADEAL_REPORT
        self.at_filters = FILTER_EDADEAL
        if self.at_project_name == 'ED':
            self.at_ym_metr += ',' + METR_ED_REGISTRATION
            ...
        elif self.at_project_name == 'EM':
            self.at_ym_metr += ',' + METR_EM_REGISTRATION
            ...
        else:
            raise ValueError("Invalid project name")

    def __set_banner_report_params(self):
        self.at_ym_dim = DIM_BANNER_REPORT
        self.at_ym_metr = METR_BANNER_REPORT
        if self.at_project_name == 'ED':
            self.at_filters = FILTER_ED_BANNER
            ...
        elif self.at_project_name == 'EM':
            self.at_filters = FILTER_EM_BANNER
            ...
        else:
            raise ValueError("Invalid project name")

    def __set_category_report_params(self):
        self.at_ym_dim = DIM_CATEGORY_REPORT
        self.at_ym_metr = METR_CATEGORY_REPORT
        self.at_filters = FILTER_CATEGORY

    @try_ping_google
    def ym_response(self):
        # параметры запроса
        params = {
            "dimensions": self.at_ym_dim,
            "metrics": self.at_ym_metr,
            "ids": self.ym_counter_id,
            "date1": self.at_start_date,
            "date2": self.at_end_date,
            # ym:s:deviceCategory!='mobile'
            "filters": self.at_filters,
            "accuracy": 1,
            "limit": self.at_limit,
            "offset": self.at_offset,
            "pretty": False,
        }

        # Формируем URL для выполнения запроса
        try:
            url = "https://api-metrika.yandex.net/stat/v1/data?"

            # Отправляем запрос к API
            headers = {"Authorization": f"OAuth {self.ym_token}"}
            response = requests.get(url, headers=headers, params=params)
            # Обрабатываем результаты
            if response.status_code != 200:
                print(
                    "Произошла ошибка при выполнении запроса:",
                    f"{response.status_code}",
                    f"{response.text}",
                )
                exit()
            else:
                data = response.json()
                self.at_total_rows = data["total_rows"]
                self.at_ym_data = data
                if self.at_total_rows == 0:
                    print("Произошла ошибка при выполнении запроса: Пустое тело ответа")
                    exit()
                return data, self.at_total_rows
        except Exception as e:
            raise e

    def ym_response_to_df(self):
        dimensions = self.at_ym_data["query"]["dimensions"]
        metrics = self.at_ym_data["query"]["metrics"]
        rows = self.at_ym_data["data"]
        rows_data = []
        for row in rows:
            dimensions_values = [dim["name"] for dim in row["dimensions"]]
            metrics_values = row["metrics"]
            row_data = dimensions_values + metrics_values
            rows_data.append(row_data)
        df = pd.DataFrame(rows_data, columns=dimensions + metrics)
        self.at_report_df = df
        return df

    def all_ym_rows_to_df(self):
        self.ym_response()
        self.ym_response_to_df()
        try:
            while (self.at_limit + self.at_offset) - 1 < self.at_total_rows:
                self.at_offset += self.at_limit
                if self.at_total_rows >= 100000 + self.at_offset - 1:
                    self.at_limit = 100000
                else:
                    self.at_limit = (
                        self.at_total_rows -
                        (self.at_limit + self.at_offset) - 1
                    )
                report_df = self.at_report_df
                self.ym_response()
                self.ym_response_to_df()
                self.at_report_df = pd.concat([report_df, self.at_report_df])
        except:
            raise "проблема с подключением"
        finally:
            return self.at_report_df
