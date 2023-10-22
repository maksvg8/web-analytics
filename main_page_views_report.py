import pandas as pd
import datetime
from typing import List
from custom_reports.modules.class_report import CustomReport
from my_selenium.modules.get_data_from_api import DataFromEDAPI
from my_selenium.config.default_configuration import *
from yandex_apis.ym_reporting_api.modules import ym_reporting_api as ym
from custom_reports.modules.banner_reporting import multiplication_metrics
from google_apis.sheets_api.modules.google_sheet_api import *
from config import (PAGE_VIEWS_SHEET_ID, PAGE_VIEWS_RANGE)



@CustomReport.try_ping_google
def page_views(project: str, start_date: str, end_date: str) -> pd.DataFrame:
    api_ed_em = DataFromEDAPI(project_name=project)
    urls = api_ed_em.get_full_df_with_urls()
    api_ed_em.get_token()
    site_map_df = api_ed_em.get_tread_data(urls)
    site_map_df.loc[0:1, H1_COLOMN] = ['Главная', 'Каталог']
    mask = site_map_df[URL_REDIR_COLOMN].str.contains(api_ed_em.at_site_url)
    filtered_df = site_map_df[mask]

    category_data = ym.YandexMetricReport('category', project, 'category_report')
    category_data.at_start_date = start_date
    category_data.at_end_date = end_date
    category_data_df = category_data.all_ym_rows_to_df()

    merged_df = pd.merge(category_data_df,
                    filtered_df,
                    left_on=['ym:pv:URLPath'],
                    right_on=['path'],
                    how='left')
    merged_df = merged_df.drop(
    ['ym:pv:URLPath', 'Status', 'Page_type', 'last_part', 'path', 'URL'],
    axis=1)

    merged_df = merged_df.drop(merged_df[(merged_df['H1'] == '') | (merged_df['H1'].isnull())].index)
    group_columns = ['ym:pv:date','URL Redir', 'H1', 'Site']
    merged_df = merged_df.groupby(group_columns, as_index=False, sort=False, dropna=False).agg('sum')
    merged_df.columns = [
        'Date', 'URL', 'H1', 'Site', 'Pageviews', 'Users'
    ]
    return merged_df



if __name__ == '__main__':
    today_dt = datetime.date.today() 
    start_date = str(today_dt - datetime.timedelta(days=90))
    end_date = str(today_dt - datetime.timedelta(days=1))
    print(start_date, end_date)
    concatenated_df = pd.DataFrame()
    projects = ['ED', 'EM']
    for project in projects:
        data = page_views(project, start_date, end_date)
        concatenated_df = pd.concat([concatenated_df, data], ignore_index=True)
    list_of_metrics = ['Pageviews', 'Users']
    concatenated_df = multiplication_metrics(concatenated_df, list_of_metrics, 10.01, 11.99)
    concatenated_df = concatenated_df.fillna('')
    clear_old_gooogle_sheet(PAGE_VIEWS_SHEET_ID, PAGE_VIEWS_RANGE)
    add_df_to_gooogle_sheets(PAGE_VIEWS_SHEET_ID, PAGE_VIEWS_RANGE, concatenated_df)
    print(concatenated_df)
    print(concatenated_df.head())
    print(concatenated_df.info())
    ...