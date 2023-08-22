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


import pandas as pd

# Создаем DataFrame для примера
data = {'Column1': [1, 2, 3],
        'Column2': ['A', 'B', 'C']}
df = pd.DataFrame(data)

# Строка, которую вы хотите добавить
new_row = [ 0, 'Z']

# Добавляем строку в начало DataFrame
df.loc[0] = new_row  # -1 для начального индекса
# df.index = df.index + 1  # Сдвигаем все индексы на 1
# df = df.sort_index()  # Сортируем DataFrame по индексу

print(df)


