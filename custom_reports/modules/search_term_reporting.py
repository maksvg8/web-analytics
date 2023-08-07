import pandas as pd
import numpy as np
import time
from credentials import DATA_DIRECTORY
from custom_reports.modules.custom_reporting import overwriting_csv

def preparation_search_terms(df):
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
    df.insert(6, 'group', True)
    return df

def set_term_group(df):
    mask1 = df['eventName'].shift(1) == df['eventName']
    mask2 = df['client_id_event'].shift(1) == df['client_id_event']
    mask3 = str(df['search_term'].shift(1)) in str(df['search_term'])
    mask4 = df['hit_timestamp'].shift(1) > df['hit_timestamp']
    mask5 = (df['hit_timestamp'].shift(1) - df['hit_timestamp']).dt.total_seconds() <= 10
    df['group'] = ~(mask1 & mask2 & mask3 & mask4 & mask5)[:-1]
    df.loc[df.index[-1], 'group'] = True
    return df

def find_zero_clicks_bots(df):
    zero_clicks_df = df.loc[
    ~df['client_id_event'].isin(
        df.loc[(df['eventName'] == 'search_complete_select')|(df['eventName'] == 'search_select'), 'client_id_event']
    )]
    zero_clicks_df["hit_timestamp"] = zero_clicks_df["hit_timestamp"].astype(str)
    return zero_clicks_df

def exclude_bots(df, exclude_df):
    df = df.loc[~df['client_id_event'].isin(exclude_df['client_id_event'])]
    return df

def drop_term_group(df):
    df = df.drop(df[df['group'] == False].index)
    df = df.drop(['group'], axis=1)
    return df

def aggregate_search_terms(df):
    df["date"] = df["date"].astype(str)
    df["hit_timestamp"] = df["hit_timestamp"].astype(str)
    agg_dict = {'eventCount': 'sum','hit_timestamp': 'nunique', 'client_id_event' : 'nunique'}
    df_grouped = df.groupby(['search_term', 'eventName','date'], as_index=False, sort=False).agg(agg_dict)
    return df_grouped