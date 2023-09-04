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
    print(000)
    df = df.sort_values(by=['client_id_event','hit_timestamp'])
    print(111)


    # mask1 = df['eventName'].shift(-1) == df['eventName']
    # mask2 = df['client_id_event'].shift(-1) == df['client_id_event']
    # mask3 = str(df['search_term'].shift(-1)) in df['search_term'][0]
    # # mask3 = df['search_term'].shift(-1) in df['search_term']
    # mask4 = df['hit_timestamp'].shift(1) > df['hit_timestamp']
    # mask5 = (df['hit_timestamp'].shift(1) - df['hit_timestamp']).dt.total_seconds() <= 10
    # # df['group'] = ~(mask1 & mask2 & mask3 & mask4 & mask5)[:-1]
    # # &mask2&mask3&mask4&mask5
 
    # df['group'] = (mask3)[1:]
    iter_time_start = time.time()
    i = 0
    while i < len(df)-1:
        mask1 = df['eventName'].iloc[i] == df['eventName'].iloc[i+1]
        mask2 = df['client_id_event'].iloc[i] == df['client_id_event'].iloc[i+1]
        mask3 = str(df['search_term'].iloc[i]) in str(df['search_term'].iloc[i+1])
        mask4 = df['hit_timestamp'].iloc[i] < df['hit_timestamp'].iloc[i+1]
        mask5 = (df['hit_timestamp'].iloc[i+1] - df['hit_timestamp'].iloc[i]).total_seconds() / 60 < 10
        if mask1 and mask2 and mask3 and mask4 and mask5:
            df.iloc[i, df.columns.get_loc('group')] = False
        else:
            df.iloc[i, df.columns.get_loc('group')] = True
        i += 1
        if i%1000 == 0:
            iter_time_1000 = time.time()
            print(i,'_',(iter_time_1000 - iter_time_start))
        elif i%100000 == 0:
            iter_time_100t = time.time()
            print(i,'_',(iter_time_100t - iter_time_start) / 60)
            iter_time_start
    print('total_',(total_time_start - time.time())/ 60)

    df.loc[df.index[-1], 'group'] = True


    # for row in df.itertuples(index=False):
    #     mask1 = df['eventName'].iloc[i] == df['eventName'].iloc[i+1]
    #     mask2 = df['client_id_event'].iloc[i] == df['client_id_event'].iloc[i+1]
    #     mask3 = str(df['search_term'].iloc[i]) in str(df['search_term'].iloc[i+1])
    #     mask4 = df['hit_timestamp'].iloc[i] < df['hit_timestamp'].iloc[i+1]
    #     mask5 = (df['hit_timestamp'].iloc[i+1] - df['hit_timestamp'].iloc[i]).total_seconds() / 60 < 10
    #     if mask1 and mask2 and mask3 and mask4 and mask5:
    #         df.iloc[i, df.columns.get_loc('group')] = False
    #     else:
    #         df.iloc[i, df.columns.get_loc('group')] = True
    #     i += 1
    #     if i%1000 == 0:
    #         iter_time_1000 = time.time()
    #         print(i,'_',(iter_time_1000 - iter_time_start))
    #     elif i%100000 == 0:
    #         iter_time_100t = time.time()
    #         print(i,'_',(iter_time_100t - iter_time_start) / 60)
    #         iter_time_start
    # print('total_',(total_time_start - time.time())/ 60)

    # df.loc[df.index[-1], 'group'] = True






    
    df.to_csv(f"C:/Users/User/Desktop/project/data/2ttttt_{file_name}.csv",index=False)
    print(222)


    
    exclude_df = df.loc[
    ~df['client_id_event'].isin(
        df.loc[(df['eventName'] == 'search_complete_select')|(df['eventName'] == 'search_select'), 'client_id_event']
    )]
    exclude_df["hit_timestamp"] = exclude_df["hit_timestamp"].astype(str)
    duplicates = ['eventName', 'hit_timestamp', 'search_term', 'client_id_event']
    file_path = f"{DATA_DIRECTORY}3ttttt_exclude_df.csv"
    try:
        old_exclude_df = pd.read_csv(file_path)
    except:
        exclude_df.to_csv(file_path, index=False)
    else:
        exclude_df = pd.concat([old_exclude_df, exclude_df])
        exclude_df.to_csv(file_path, index=False)
    df = df.loc[~df['client_id_event'].isin(exclude_df['client_id_event'])]

    df = df.drop(df[df['group'] == False].index)
    df = df.drop(['group'], axis=1)
    print('333_total_',(total_time_start - time.time())/ 60)



    df_for_pivot = df.copy()
    # unique_events = df['eventName'].unique().tolist() 
    agg_dict = {'search_term': 'nunique', 'hit_timestamp' : 'nunique'}
    pivot_df = df_for_pivot.pivot_table(index='client_id_event', columns='eventName',
                            values=['search_term','hit_timestamp'], 
                            aggfunc=agg_dict, 
                            fill_value=0)
    # pivot_df.columns = ['ev_search', 'ev_search_complete', 'ev_search_complete_select', 'ev_search_select', 'terms_search', 'terms_search_complete', 'terms_search_complete_select', 'terms_search_select']

    pivot_df = pivot_df.reset_index()
    # Переименовываем столбцы и суммируем значения для столбца 'eventName'
    # pivot_df['sum'] = pivot_df['A'] + pivot_df['B']

    pivot = CustomReport('pivot', 'ed', 'search')
    pivot.overwriting_old_csv_report(pivot_df, f'4ttttt_pivot_{file_name}')
    print('444_total_',(total_time_start - time.time())/ 60)

    # Добавить группировку по новому столбцу даты

    df["date"] = df["date"].astype(str)
    df["hit_timestamp"] = df["hit_timestamp"].astype(str)
    agg_dict = {'eventCount': 'sum','hit_timestamp': 'nunique', 'client_id_event' : 'nunique'}
    df_grouped = df.groupby(['search_term', 'eventName','date'], as_index=False, sort=False).agg(agg_dict)
    # df_grouped = df_grouped.drop(df_grouped[((df_grouped['eventName'] == 'search') | (df_grouped['eventName'] == 'search_complete' )) & (df_grouped['client_id_event'] < 2)].index)
    df_grouped.to_csv(f"C:/Users/User/Desktop/project/data/5ttttt_agg2_{file_name}.csv",index=False)
    print('555_total_',(total_time_start - time.time())/ 60)

    return df_grouped

if __name__ == "__main__":
    df = pd.read_csv(f"{DATA_DIRECTORY}ed_default_search_term_july.csv")
    aggregate_search_terms(df, "search_term_july")