import pandas as pd
import datetime
from typing import List
from custom_reports.modules.class_report import CustomReport
from my_selenium.modules.get_data_from_api import GetDataFromAPI
from my_selenium.config.default_configuration import *
from yandex_apis.ym_reporting_api.modules import ym_reporting_api as ym
from custom_reports.modules.banner_reporting import *
from google_apis.sheets_api.modules.google_sheet_api import *



from config import (PAGE_VIEWS_SHEET_ID, PAGE_VIEWS_ED_RANGE, PAGE_VIEWS_EM_RANGE)



@CustomReport.try_ping_google
def page_views(project: str, start_date: [str], end_date: str) -> pd.DataFrame:
    api_ed_em = GetDataFromAPI(project_name=project)
    urls = api_ed_em.get_full_df_with_urls()
    api_ed_em.get_token()
    site_map_df = api_ed_em.get_async_data(urls)
    site_map_df.loc[0:1, H1_COLOMN] = ['Главная', 'Каталог']
    category_data = ym.YandexMetricReport('category', project, 'category_report')
    category_data.at_start_date = start_date
    category_data.at_end_date = end_date
    category_data_df = category_data.all_ym_rows_to_df()
    print(category_data_df)
    merged_df = pd.merge(category_data_df,
                    site_map_df,
                    left_on=['ym:pv:URLPath'],
                    right_on=['path'],
                    how='left')
    print(merged_df)
    merged_df = merged_df.drop(
    ['ym:pv:date', 'ym:pv:URLPath', 'Site', 'Page_type', 'last_part', 'path', 'URL Redir'],
    axis=1)

    # def contains_partial(row):
    #     mask1 = row['eventName'] == row['eventName_']
    #     mask2 = row['client_id_event'] == row['client_id_event_']
    #     mask3 = str(row['search_term']) in str(row['search_term_'])
    #     mask4 = row['hit_timestamp_'] > row['hit_timestamp']
    #     mask5 = (row['hit_timestamp_'] - row['hit_timestamp']).seconds / 60 <= 10
    #     result = not (mask1 & mask2 & mask3 & mask4 & mask5)
    #     return result
    
    # df['group'] = df.apply(lambda row: contains_partial(row), axis=1)



    merged_df = merged_df.drop(merged_df[(merged_df['Status'] != '200') | (merged_df['H1'] == '')].index)
    group_columns = [
    'URL', 'H1', 'Status']
    merged_df = merged_df.groupby(group_columns, as_index=False, sort=False, dropna=False).agg('sum')
    merged_df.columns = [
        'URL', 'H1', 'Status', 'pageviews', 'users'
    ]
    print(merged_df)
    final_data = CustomReport('page_views_data', project, 'category_report')
    final_data.overwriting_old_csv_report(merged_df)
    # df_reindexed = df_reindexed.fillna('')
    # clear_old_gooogle_sheet(PAGE_VIEWS_SHEET_ID, "'Факт Август'!A1:P")
    # add_df_to_gooogle_sheets(PAGE_VIEWS_SHEET_ID, "'Факт Август'!A1:P", merged_df)
    return merged_df

    # df_reindexed = grouped_df.reindex(columns=[
    #     'Project', 'Source', 'Direction', 'UTMCapaigne',
    #     'Account Currency', 'Visits','Users', 'Purchases', 'Revenue', 'Registration', 'Goal',
    #     'Clicks', 'Impressions', 'Daily Budget', 'Budget', 'Cost'
    # ])



if __name__ == '__main__':
    today_dt = datetime.date.today() 
    start_date = str(today_dt - datetime.timedelta(days=90))
    start_date = '2023-08-01'
    end_date = str(today_dt - datetime.timedelta(days=1))
    end_date = '2023-08-31'
    print(start_date, end_date)
    # 'ED',
    projects = [ 'EM']
    for project in projects:
        data = page_views(project, start_date, end_date)
        if project == 'ED':
            SHEET_RANGE = PAGE_VIEWS_ED_RANGE
        elif project == 'EM':
            SHEET_RANGE = PAGE_VIEWS_EM_RANGE
        else:
            raise ValueError('Invalid project name')
        df_reindexed = data.fillna('')
        clear_old_gooogle_sheet(PAGE_VIEWS_SHEET_ID, SHEET_RANGE)
        add_df_to_gooogle_sheets(PAGE_VIEWS_SHEET_ID, SHEET_RANGE, df_reindexed)
        print(data.head())
        print(data.info())

    ...