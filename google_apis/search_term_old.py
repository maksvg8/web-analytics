import pandas as pd
import numpy as np
import urllib.parse
import time
start_time_all = time.time()
df = pd.read_csv("C:/Users/User/Desktop/python/data/ed_custom_ga4_search_term_may.csv", dtype={"customEvent:search_term": object, "customEvent:client_id_event": object})
print(df.info())
df.columns = ['eventName', 'hit_timestamp', 'search_term', 'client_id_event', 'eventCount']
df['search_term'] = df.search_term.str.lower().str.strip()
df['hit_timestamp'] = df.hit_timestamp.str.strip()
df["hit_timestamp"] = df["hit_timestamp"].str.replace('\+.*', '', regex=True)
df["hit_timestamp"] = df["hit_timestamp"].str.replace('-\d\d:.*', '', regex=True)
df["hit_timestamp"] = df["hit_timestamp"].str.replace('\..*', '', regex=True)
# df["hit_timestamp2"] = df["hit_timestamp"].str.replace('T.*', '', regex=True)
# df["hit_timestamp2"] = pd.to_datetime(df["hit_timestamp"].str.replace('T.*', '', regex=True), format='%Y-%m-%d')
df["hit_timestamp"] = pd.to_datetime(df["hit_timestamp"], format='%Y-%m-%dT%H:%M:%S')
df.insert(5, 'group', True)
print(df.head())

start_time = time.time()
j = 0
# i = 0
for i in range(len(df)-1):
    mask1 = df['eventName'].iloc[i] == df['eventName'].iloc[i+1]
    mask2 = df['client_id_event'].iloc[i] == df['client_id_event'].iloc[i+1]
    mask3 = str(df['search_term'].iloc[i]) in str(df['search_term'].iloc[i+1])
    mask4 = df['hit_timestamp'].iloc[i] < df['hit_timestamp'].iloc[i+1]
    mask5 = (df['hit_timestamp'].iloc[i+1] - df['hit_timestamp'].iloc[i]).total_seconds() <= 10
    if mask1 and mask2 and mask3 and mask4:
        df.loc[df.index[i], 'group'] = False
        # df.loc[df.index[i+1], 'eventCount'] += 1
        # df.loc[df.index[i+1], 'sessions'] += 1
    else:
        df.loc[df.index[i], 'group'] = True
    j+=1
    if j % 100000 == 0:
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"{j} {elapsed_time}")
        start_time = end_time
    # i += 1

df.loc[df.index[-1], 'group'] = True
df.to_csv("C:/Users/User/Desktop/python/data/ed_custom_ga4_search_term_may_com.csv",index=False)
df = df.drop(df[df['group'] == False].index)
df = df.drop(['group'], axis=1)

df = pd.read_csv("C:/Users/User/Desktop/python/data/ed_custom_ga4_search_term_may_com.csv")

print(df.info())
df["hit_timestamp"] = df["hit_timestamp"].astype(str)
agg_dict = {'eventCount': 'sum','hit_timestamp': 'nunique', 'client_id_event' : 'nunique'}
df_grouped = df.groupby(['search_term', 'eventName'], as_index=False, sort=False).agg(agg_dict)
# df_grouped = df_grouped.drop(df_grouped[((df_grouped['eventName'] == 'search') | (df_grouped['eventName'] == 'search_complete' )) & (df_grouped['client_id_event'] < 2)].index)
df_grouped.to_csv("C:/Users/User/Desktop/python/data/ed_custom_ga4_search_term_june_complete_2.csv",index=False)


print(df_grouped.info())
df_pivot_table = df_grouped.pivot_table(index='search_term',
                                columns='eventName',
                                values=['eventCount', 'hit_timestamp', 'client_id_event'])



# df_pivot_table.to_excel("C:/Users/User/Desktop/python/data/ed_custom_ga4_search_term_complete_term2.xlsx")
print(df_pivot_table.head())

end_time_all = time.time()
elapsed_time = end_time_all - start_time_all
print(f"{elapsed_time}  {elapsed_time/ 3600}")