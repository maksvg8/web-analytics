import pandas as pd
import numpy as np
import time
from credentials import DATA_DIRECTORY
from custom_reports.modules.class_report import CustomReport
from custom_reports.modules.search_term_reorting import *


df = pd.read_csv(f"{DATA_DIRECTORY}ed_default_search_term_may.csv")
df = preparation_search_terms(df)
df = set_term_group(df)
zero_clicks_df = find_zero_clicks_bots(df)

unique_events = df['eventName'].unique().tolist() 
agg_dict = {'search_term': 'nunique', 'hit_timestamp' : 'nunique', 'eventCount': 'sum'}
pivot_df = df.pivot_table(index='client_id_event', columns='eventName',
                           values=['search_term','hit_timestamp','eventCount'], 
                           aggfunc=agg_dict, 
                           fill_value=0)

# Переименовываем столбцы и суммируем значения для столбца 'eventName'
# pivot_df.columns = unique_events
# pivot_df['sum'] = pivot_df['A'] + pivot_df['B']

print(pivot_df)

zero_clicks = CustomReport('zero_clicks', 'ed', 'search')
zero_clicks_df = zero_clicks.overwriting_old_csv_report(zero_clicks_df, 'exclude_df')

# df = exclude_bots(df, zero_clicks_df)
# df = drop_term_group(df)
# df = aggregate_search_terms(df)
# search_term = CustomReport('search_term', 'ed', 'search')
# search_term.overwriting_old_csv_report(zero_clicks_df, 'agg_search_term_may')
