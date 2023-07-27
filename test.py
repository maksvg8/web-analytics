import pandas as pd
from datetime import timedelta, datetime
import ym_reporting_api as ym
from custom_reporting import *
from google_sheet_api import *
from credentials import DATA_DIRECTORY
from config import (COAST_SHEET_ID, COAST_SHEET_RANGE, PLAN_SHEET_ID, PLAN_SHEET_RANGE_JUNE, REPORT_SHEET_RANGE)
from credentials import GA4_ED_PROPERTY_ID


# report_ed = ym.YandexMetricReport('ym_test', 'ed', 'campaign_report')
# report_ed.at_start_date = '2023-06-01'
# # reportED.atEndDate = '2023-06-18'
# data_ed = report_ed.all_ym_rows_to_df()
# print(data_ed.head())

# cost_data = get_rows_from_gooogle_sheets("COAST_SHEET_ID", COAST_SHEET_RANGE)




# Создаем исходный датафрейм
data = {
    'eventName': ['event1', 'event1', 'event1', 'event2', 'event2', 'event2'],
    'hit_timestamp': ['2023-06-01', '2023-06-02', '2023-06-03', '2023-06-01', '2023-06-02', '2023-06-03'],
    'search_term': ['term1', 'term2', 'term3', 'term1', 'term2', 'term3'],
    'client_id_event': ['client1', 'client1', 'client1', 'client2', 'client2', 'client2'],
    'eventCount': [1, 2, 3, 1, 2, 3],
    'group': [True, False, False, True, False, False]
}

df = pd.DataFrame(data)

# Преобразуем столбец hit_timestamp в тип datetime
df['hit_timestamp'] = pd.to_datetime(df['hit_timestamp'])

# # Создаем столбец, в котором будет определяться новая группа
# df['new_group'] = df['group'] != df['group'].shift(1)

# # Заполняем пропущенные значения столбца new_group значением False
# df['new_group'].fillna(False, inplace=True)

# Группируем данные
grouped_df = df.groupby(['eventName', 'search_term', 'group']).agg({
    'hit_timestamp': 'min',
    'client_id_event': 'first',
    'eventCount': 'sum',

}).reset_index()

# Удаляем вспомогательный столбец new_group
# grouped_df.drop(columns='new_group', inplace=True)

# Выводим результат
print(grouped_df)
print(GA4_ED_PROPERTY_ID)