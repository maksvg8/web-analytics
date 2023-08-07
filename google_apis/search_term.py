import pandas as pd
import numpy as np
import time
from credentials import DATA_DIRECTORY
from custom_reports.modules.custom_reporting import overwriting_csv

def aggregate_search_terms(df = pd.DataFrame(), file_name = ""):
    start_time_all = time.time()
    df.columns = ['eventName', 'hit_timestamp', 'search_term', 'client_id_event', 'eventCount']
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



    



    mask1 = df['eventName'].shift(-1) == df['eventName']
    mask2 = df['client_id_event'].shift(-1) == df['client_id_event']
    mask3 = df['search_term'].shift(-1).isin(df['search_term'])
    # mask3 = df['search_term'].shift(-1) in df['search_term']
    mask4 = df['hit_timestamp'].shift(1) > df['hit_timestamp']
    mask5 = (df['hit_timestamp'].shift(1) - df['hit_timestamp']).dt.total_seconds() <= 10
    # df['group'] = ~(mask1 & mask2 & mask3 & mask4 & mask5)[:-1]
    # &mask2&mask3&mask4&mask5
    print(mask3)
    df['group'] = (mask3)[1:]
    # df.loc[df.index[-1], 'group'] = True

    print(df.info())
    print(df.describe())
    # unique_events = df['group'].unique().tolist()
    # print(unique_events)
    df.to_csv(f"C:/Users/User/Desktop/project/data/{file_name}.csv",index=False)
    

    
    exclude_df = df.loc[
    ~df['client_id_event'].isin(
        df.loc[(df['eventName'] == 'search_complete_select')|(df['eventName'] == 'search_select'), 'client_id_event']
    )]
    exclude_df["hit_timestamp"] = exclude_df["hit_timestamp"].astype(str)
    duplicates = ['eventName', 'hit_timestamp', 'search_term', 'client_id_event']
    file_path = f"{DATA_DIRECTORY}exclude_df.csv"
    try:
        old_exclude_df = pd.read_csv(file_path)
    except:
        exclude_df.to_csv(file_path, index=False)
    else:
        exclude_df = pd.concat([old_exclude_df, exclude_df]).drop_duplicates(subset=duplicates)
        exclude_df.to_csv(file_path, index=False)
    df = df.loc[~df['client_id_event'].isin(exclude_df['client_id_event'])]

    df = df.drop(df[df['group'] == False].index)
    df = df.drop(['group'], axis=1)


    # Добавить группировку по новому столбцу даты

    df["date"] = df["date"].astype(str)
    df["hit_timestamp"] = df["hit_timestamp"].astype(str)
    agg_dict = {'eventCount': 'sum','hit_timestamp': 'nunique', 'client_id_event' : 'nunique'}
    df_grouped = df.groupby(['search_term', 'eventName','date'], as_index=False, sort=False).agg(agg_dict)
    # df_grouped = df_grouped.drop(df_grouped[((df_grouped['eventName'] == 'search') | (df_grouped['eventName'] == 'search_complete' )) & (df_grouped['client_id_event'] < 2)].index)
    df_grouped.to_csv(f"C:/Users/User/Desktop/project/data/agg_{file_name}.csv",index=False)


    return df_grouped

if __name__ == "__main__":
    df = pd.read_csv(f"{DATA_DIRECTORY}ed_default_search_term_may.csv")
    aggregate_search_terms(df, "ttttttttttt")