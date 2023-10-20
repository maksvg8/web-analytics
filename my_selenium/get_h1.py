import pandas as pd
import datetime
from typing import List
from custom_reports.modules.class_report import CustomReport
from my_selenium.modules.get_data_from_api import DataFromEDAPI
from my_selenium.config.default_configuration import *
from yandex_apis.ym_reporting_api.modules import ym_reporting_api as ym
from google_apis.sheets_api.modules.google_sheet_api import *





if __name__ == '__main__':
    concatenated_df = pd.DataFrame()
    project_name_list = ['ED', 'EM']
    for project in project_name_list:
        test = DataFromEDAPI(project_name=project)
        urls = test.get_full_df_with_urls()
        test.get_token()
        site_map_df = test.get_tread_data(urls)
        site_map_df.loc[0:1, H1_COLOMN] = ['Главная', 'Каталог']
        print(site_map_df)
        test = CustomReport('test', 'ED')
        test.overwriting_old_csv_report(site_map_df, f'site_map_{project}')
        concatenated_df = pd.concat([concatenated_df, site_map_df], ignore_index=True)
    print(concatenated_df)