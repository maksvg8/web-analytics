import pandas as pd
import datetime
from yandex_apis.ym_reporting_api.modules import ym_reporting_api as ym
from custom_reports.modules.campaign_reporting import *
from custom_reports.modules.class_report import *
from google_apis.sheets_api.modules.google_sheet_api import *
from google_apis.data_api.modules import ga4_reporting_v1 as ga4
from credentials import DATA_DIRECTORY
from config import (COAST_SHEET_ID, COAST_SHEET_RANGE, PLAN_SHEET_ID, PLAN_SHEET_RANGE_JUNE, PLAN_SHEET_RANGE_JULY, PLAN_SHEET_RANGE_AUGUST, REPORT_SHEET_RANGE)

from google_apis.data_api.config.default_configuration import (ga4_dim_banners, ga4_metr_banners, ga4_dim_transaction,
                    ga4_metr_transaction, ga4_dim_ed_search,
                    ga4_metr_ed_search, ga4_dim_funnel, ga4_metr_funnel,
                    ga4_dim_List, ga4_metr_List, ga4_dim_transaction_email,
                    ga4_metr_transaction_email, ga4_dim_sessionManualTerm,
                    ga4_metr_sessionManualTerm,ga4_dim_search_term,ga4_metr_search_term,ga4_dim_custom,ga4_metr_custom)


data = {'A': [3, 1, 2, 1, 2],
        'B': [6, 4, 5, 2, 3]}

data2 = {'A': [3, 1, 2, 1, 123123123],
        'B': [6, 12312, 5, 2, 3]}


df = pd.DataFrame(data2)

# test = ym.YandexMetricReport('sraka', 'ED', 'campaign_report')
# data = test.all_ym_rows_to_df()
report = ga4.GA4Report("ga4_1223123123123", "ed")
report.at_start_date = "2023-07-01"
report.at_end_date = "2023-08-20"
report.at_ga4_dim_list = ga4_dim_search_term
report.at_ga4_metr_list = ga4_metr_search_term
df = report.ga4_all_rows_to_df()
print(df)
# report.try_ping_google()
# report.overwriting_old_csv_report(data)


