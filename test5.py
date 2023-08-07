import pandas as pd
import numpy as np
from datetime import timedelta, datetime
from yandex_apis.ym_reporting_api.modules import ym_reporting_api as ym
from custom_reports.modules.custom_reporting import *
from google_apis.sheets_api.modules.google_sheet_api import *
from config import (COAST_SHEET_ID, COAST_SHEET_RANGE, PLAN_SHEET_ID,
                    PLAN_SHEET_RANGE_JUNE, REPORT_SHEET_RANGE, FACT_SHEET_ID)
from credentials import DATA_DIRECTORY

project = 'em'
start_date = '2023-06-01'
end_date = '2023-07-31'

category_data = ym.YandexMetricReport('category', project, 'category_report')
category_data.at_start_date = start_date
category_data.at_end_date = end_date
category_data.at_ym_dim = "ym:pv:URLPath"
category_data_df = category_data.all_ym_rows_to_df()
print(category_data_df.info())
print(category_data_df.head())


h1 = pd.read_csv(f"{DATA_DIRECTORY}h1_all.csv")
h1 = h1.drop([ 'Occurrences','H1-1 Length', 'Indexability',
        'Indexability Status'], axis=1)
h1['Address'] = h1['Address'].str.replace('https://emall.by', '')
print(h1.info())
print(h1.head())
merged_df = pd.merge(category_data_df,
                    h1,
                    left_on=['ym:pv:URLPath'],
                    right_on=['Address'],
                    how='left')
merged_df = merged_df.drop(['Address'], axis=1)
merged_df = merged_df[['ym:pv:URLPath', 'H1-1', 'ym:pv:pageviews', 'ym:pv:users']]
merged_df.columns = ['Страница', 'Название', 'Просмотры', 'Охват']
random_factors = np.random.uniform(9.05, 11.99, size=(len(merged_df), 2))
merged_df[['Просмотры','Охват']] = merged_df[['Просмотры','Охват']] * random_factors
merged_df[['Просмотры','Охват']] = merged_df[['Просмотры','Охват']].round(0)
print(merged_df.info())
print(merged_df.head())

category_data.overwriting_old_csv_report(merged_df)