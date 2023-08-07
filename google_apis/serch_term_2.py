import pandas as pd
import numpy as np
import time
from credentials import DATA_DIRECTORY
from custom_reports.modules.class_report import CustomReport
from custom_reports.modules.search_term_reporting import *


df = pd.read_csv(f"{DATA_DIRECTORY}ed_default_search_term_july.csv")
df = preparation_search_terms(df)
df = set_term_group(df)
print(df.info())
print(df.describe())
unique_events = df['group'].unique().tolist()
print(unique_events)
search_term = CustomReport('search_term', 'ed', 'search')
search_term.overwriting_old_csv_report(df, 'agg_search_term_july3')
zero_clicks_df = find_zero_clicks_bots(df)



# df_for_pivot = df.copy()
# # unique_events = df['eventName'].unique().tolist() 
# agg_dict = {'search_term': 'nunique', 'hit_timestamp' : 'nunique'}
# pivot_df = df_for_pivot.pivot_table(index='client_id_event', columns='eventName',
#                            values=['search_term','hit_timestamp'], 
#                            aggfunc=agg_dict, 
#                            fill_value=0)
# pivot_df.columns = ['ev_search', 'ev_search_complete', 'ev_search_complete_select', 'ev_search_select', 'terms_search', 'terms_search_complete', 'terms_search_complete_select', 'terms_search_select']

# pivot_df = pivot_df.reset_index()
# # Переименовываем столбцы и суммируем значения для столбца 'eventName'
# # pivot_df['sum'] = pivot_df['A'] + pivot_df['B']

# print(type(pivot_df))
# print(pivot_df)
# pivot = CustomReport('pivot', 'ed', 'search')
# pivot.overwriting_old_csv_report(pivot_df, 'pivot_df')



# zero_clicks = CustomReport('zero_clicks', 'ed', 'search')
# zero_clicks_df = zero_clicks.overwriting_old_csv_report(zero_clicks_df, 'exclude_df')

# df = exclude_bots(df, zero_clicks_df)
# df = drop_term_group(df)
# df = aggregate_search_terms(df)
# search_term = CustomReport('search_term', 'ed', 'search')
# search_term.overwriting_old_csv_report(df, 'agg_search_term_july2')
