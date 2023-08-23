from google_apis.data_api.modules import ga4_reporting_v1 as ga4
import pandas as pd
from google_apis.data_api.config.default_configuration import *
from credentials import DATA_DIRECTORY

# report = ga4.GA4Report("ga4", "ED")
# report.at_start_date = "2023-07-01"
# report.at_end_date = "2023-08-22"
# report.at_ga4_dim_list = ga4_dim_ed_sign_up_users
# report.at_ga4_metr_list = ga4_metr_ed_sign_up_users
# report.at_offset = 0
# report.at_limit = 100000

# df = report.ga4_all_rows_to_df()
# report.overwriting_old_csv_report(df)
df = pd.read_csv(f'{DATA_DIRECTORY}ED_default_ga4')

df.columns = ['date', 'hit_timestamp', 'eventName', 'user_id', 'events']

df[['search_term', 'client_id_event']] = df[['search_term', 'client_id_event']].astype(object)
df['eventCount'] = df['eventCount'].astype(float)
df['search_term'] = df.search_term.str.lower().str.strip()
df['hit_timestamp'] = df.hit_timestamp.str.strip()
df["hit_timestamp"] = df["hit_timestamp"].str.replace('\+.*', '', regex=True)
df["hit_timestamp"] = df["hit_timestamp"].str.replace('-\d\d:.*', '', regex=True)
df["hit_timestamp"] = df["hit_timestamp"].str.replace('\..*', '', regex=True)
df["date"] = pd.to_datetime(df["hit_timestamp"].str.replace('T.*', '', regex=True), format='%Y-%m-%d')
df["hit_timestamp"] = pd.to_datetime(df["hit_timestamp"], format='%Y-%m-%dT%H:%M:%S')
df.insert(6, 'group', '')
print(000)
df = df.sort_values(by=['client_id_event','hit_timestamp'])
print(111)