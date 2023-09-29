import pandas as pd
import numpy as np
import time
from credentials import DATA_DIRECTORY
from custom_reports.modules.class_report import CustomReport

def aggregate_search_terms(df = pd.DataFrame(), file_name = ""):
    total_time_start = time.time()
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
    print('111_',(time.time()- total_time_start) / 60)

    df = df.sort_values(by=['client_id_event','hit_timestamp']).reset_index(drop=True)
    print('222_',(time.time()- total_time_start) / 60)

    df[['eventName_', 'hit_timestamp_', 'search_term_', 'client_id_event_']] = df[['eventName', 'hit_timestamp', 'search_term', 'client_id_event']].shift(-1)
    print('333_',(time.time()- total_time_start) / 60)

    def contains_partial(row):
        mask1 = row['eventName'] == row['eventName_']
        mask2 = row['client_id_event'] == row['client_id_event_']
        mask3 = str(row['search_term']) in str(row['search_term_'])
        mask4 = row['hit_timestamp_'] > row['hit_timestamp']
        mask5 = (row['hit_timestamp_'] - row['hit_timestamp']).seconds / 60 <= 10
        result = not (mask1 & mask2 & mask3 & mask4 & mask5)
        if row.name%100000 == 0:
            print('total_', row.name, ' ',(time.time() - total_time_start)/ 60)
        return result
    
    df['group'] = df.apply(lambda row: contains_partial(row), axis=1)
    print('444_',(time.time()- total_time_start) / 60)

    df = df.drop(['eventName_', 'hit_timestamp_', 'search_term_', 'client_id_event_'], axis=1)
    print('555_',(time.time()- total_time_start) / 60)

    # 
    df.to_csv(f"C:/Users/User/Desktop/project/data/{file_name}_with_group.csv",index=False)
    print('666_',(time.time()- total_time_start) / 60)


    
    exclude_df = df.loc[
    ~df['client_id_event'].isin(
        df.loc[(df['eventName'] == 'search_complete_select')|(df['eventName'] == 'search_select'), 'client_id_event']
    )]
    exclude_df["hit_timestamp"] = exclude_df["hit_timestamp"].astype(str)
    duplicates = CustomReport('pivot', 'ED', 'search')
    exclude_df = duplicates.overwriting_old_csv_report(exclude_df, 'exclude_df')
    df = df.loc[~df['client_id_event'].isin(exclude_df['client_id_event'])]

    df = df.drop(df[df['group'] == False].index)
    df = df.drop(['group'], axis=1)
    print('777_',(time.time() - total_time_start) / 60)



    df_for_pivot = df.copy()
    # unique_events = df['eventName'].unique().tolist() 
    agg_dict = {'search_term': 'nunique', 'hit_timestamp' : 'nunique'}
    pivot_df = df_for_pivot.pivot_table(index='client_id_event', columns='eventName',
                            values=['search_term','hit_timestamp'], 
                            aggfunc=agg_dict, 
                            fill_value=0)

    pivot_df = pivot_df.reset_index()
    pivot = CustomReport('pivot', 'ED', 'search')
    pivot.overwriting_old_csv_report(pivot_df, f'{file_name}_pivot')
    print('888_',(time.time() - total_time_start) / 60)

    # Добавить группировку по новому столбцу даты
    df["date"] = df["date"].astype(str)
    df["hit_timestamp"] = df["hit_timestamp"].astype(str)
    agg_dict = {'eventCount': 'sum','hit_timestamp': 'nunique', 'client_id_event' : 'nunique'}
    df_grouped = df.groupby(['search_term', 'eventName','date'], as_index=False, sort=False).agg(agg_dict)
    final_df = CustomReport('final_agg', 'ED', 'search')
    final_df.overwriting_old_csv_report(df_grouped, f'final_agg_{file_name}')
    print('999_',(time.time() - total_time_start) / 60)

    return df_grouped

if __name__ == "__main__":
    name = 'search_term_aug'
    df = pd.read_csv(f"{DATA_DIRECTORY}ED_default_{name}.csv")
    aggregate_search_terms(df, name)