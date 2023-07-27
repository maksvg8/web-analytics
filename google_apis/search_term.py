import pandas as pd
import numpy as np
import time

def aggregate_search_terms(df, file_name):
    start_time_all = time.time()
    df.columns = ['eventName', 'hit_timestamp', 'search_term', 'client_id_event', 'eventCount']
    df[['search_term', 'client_id_event']] = df[['search_term', 'client_id_event']].astype(object)
    df['search_term'] = df.search_term.str.lower().str.strip()
    df['hit_timestamp'] = df.hit_timestamp.str.strip()
    df["hit_timestamp"] = df["hit_timestamp"].str.replace('\+.*', '', regex=True)
    df["hit_timestamp"] = df["hit_timestamp"].str.replace('-\d\d:.*', '', regex=True)
    df["hit_timestamp"] = df["hit_timestamp"].str.replace('\..*', '', regex=True)
    df["date"] = pd.to_datetime(df["hit_timestamp"].str.replace('T.*', '', regex=True), format='%Y-%m-%d')
    df["hit_timestamp"] = pd.to_datetime(df["hit_timestamp"], format='%Y-%m-%dT%H:%M:%S')
    df.insert(6, 'group', True)



    start_time = time.time()

    mask1 = df['eventName'].shift(1) == df['eventName']
    mask2 = df['client_id_event'].shift(1) == df['client_id_event']
    mask3 = str(df['search_term'].shift(1)) in str(df['search_term'])
    mask4 = df['hit_timestamp'].shift(1) > df['hit_timestamp']
    mask5 = (df['hit_timestamp'].shift(1) - df['hit_timestamp']).dt.total_seconds() <= 10
    df['group'] = ~(mask1 & mask2 & mask3 & mask4 & mask5)[:-1]
    df.loc[df.index[-1], 'group'] = True
    df = df.drop(df[df['group'] == False].index)
    df = df.drop(['group'], axis=1)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"{elapsed_time}")
    start_time = end_time

    # Добавить группировку по новому столбцу даты

    df["date"] = df["date"].astype(str)
    df["hit_timestamp"] = df["hit_timestamp"].astype(str)
    agg_dict = {'eventCount': 'sum','hit_timestamp': 'nunique', 'client_id_event' : 'nunique'}
    df_grouped = df.groupby(['search_term', 'eventName','date'], as_index=False, sort=False).agg(agg_dict)
    # df_grouped = df_grouped.drop(df_grouped[((df_grouped['eventName'] == 'search') | (df_grouped['eventName'] == 'search_complete' )) & (df_grouped['client_id_event'] < 2)].index)
    df_grouped.to_csv(f"C:/Users/User/Desktop/python/data/agg_{file_name}.csv",index=False)

    end_time_all = time.time()
    elapsed_time = end_time_all - start_time_all
    print(f"{elapsed_time}  {elapsed_time/ 60}")
    return df_grouped

if __name__ == "__main__":
    df = pd.read_csv("C:/Users/User/Desktop/python/data/ed_custom_ga4_search_term_apr.csv")
    aggregate_search_terms(df, "tttt")