import pandas as pd
import numpy as np

data = {'A': [3, 1, 2, 1, 2],
        'B': [6, 4, 5, 2, 3]}

df = pd.DataFrame(data)

df[['A','B']] = 0, 1

def test(c, *args):
    for aa in args:
        print(aa, type(aa))
    return args


import pandas as pd
import datetime
from yandex_apis.ym_reporting_api.modules import ym_reporting_api as ym
from custom_reports.modules.custom_reporting import *
from google_apis.sheets_api.modules.google_sheet_api import *
from credentials import DATA_DIRECTORY
from config import (COAST_SHEET_ID, COAST_SHEET_RANGE, PLAN_SHEET_ID, PLAN_SHEET_RANGE_JUNE, PLAN_SHEET_RANGE_JULY, PLAN_SHEET_RANGE_AUGUST, REPORT_SHEET_RANGE)

start_date = datetime.date.today() - datetime.timedelta(days=60)

cost_data = get_rows_from_gooogle_sheets(COAST_SHEET_ID, COAST_SHEET_RANGE)

report_ed = ym.YandexMetricReport('ym_main_cost', 'ED', 'campaign_report')
report_ed.at_start_date = start_date
report_ed.at_project_name
data_ed = report_ed.all_ym_rows_to_df()
data_ed = transform_ym_ed_em_campaign_dfs(data_ed, report_ed.at_project_name)

report_em = ym.YandexMetricReport('ym_main_cost', 'EM', 'campaign_report')
report_em.at_start_date = start_date
data_em = report_em.all_ym_rows_to_df()
data_em = transform_ym_ed_em_campaign_dfs(data_em, report_em.at_project_name)

report_jb = ym.YandexMetricReport('ym_main_cost', 'JB', 'campaign_report')
report_jb.at_start_date = start_date
data_jb = report_jb.all_ym_rows_to_df()
data_jb = transform_ym_jb_campaign_df(data_jb)

data_ed, data_em, data_jb = rename_campaign_df(data_ed, data_em, data_jb)
concatenated_ym_df = concat_ym_campaign_dfs(data_ed, data_em, data_jb)
merged_df = merge_ym_capaigne_df_and_costs_data(concatenated_ym_df, cost_data)
print(merged_df)

