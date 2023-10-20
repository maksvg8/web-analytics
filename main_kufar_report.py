import pandas as pd
from datetime import timedelta, datetime
from yandex_apis.ym_reporting_api.modules import ym_reporting_api as ym
from google_apis.sheets_api.modules.google_sheet_api import *
from config import (KUFAR_SHEET_ID, KUFAR_SHEET_RANGE)

report_data = extract_rows_from_gooogle_sheets(KUFAR_SHEET_ID, KUFAR_SHEET_RANGE)
if report_data.empty == False:
    report_data['Дата'] = pd.to_datetime(report_data['Дата'])
    start_date = report_data['Дата'].max() + timedelta(days=1)
    start_date = start_date.strftime('%Y-%m-%d')
    end_date = datetime.today()- timedelta(days=1)
    end_date = end_date.strftime('%Y-%m-%d')
else:
    start_date = '2023-07-03'
    end_date = '2023-07-23'

report_em_kufar = ym.YandexMetricReport('ym_kufar', 'EM', 'kufar_report')
report_em_kufar.at_start_date = start_date
report_em_kufar.at_end_date = end_date
data_em = report_em_kufar.all_ym_rows_to_df()
data_em.columns = [
    'Дата', 'UTMSource', 'UTMCampaign', 'UTMMedium', 'UTMContent', 'UTMTerm', 'ID_Покупки',
    'Визиты','Пользователи', 'Покупки', 'Доход', 'Регистрации'
]
# report_em_kufar.overwriting_old_csv_report(data_em, 'test_test_test')
final_df = data_em.fillna('')
del_data = clear_old_gooogle_sheet(KUFAR_SHEET_ID, KUFAR_SHEET_RANGE)
set_data = add_df_to_gooogle_sheets(KUFAR_SHEET_ID, KUFAR_SHEET_RANGE, final_df)
print(111)