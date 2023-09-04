import pandas as pd
import numpy as np
import time
from credentials import DATA_DIRECTORY
from custom_reports.modules.class_report import CustomReport
from custom_reports.modules.custom_reporting import overwriting_csv


# Создание датафрейма для примера
data = {'A': [3, 1, 2, 1, 2],
        'B': [6, 4, 5, 2, 3]}
df = pd.DataFrame(data)

# Сортировка по столбцам 'A' и 'B'


def aggregate_search_terms(df=pd.DataFrame(), file_name=""):
    total_time_start = time.time()
    iter_time_start = time.time()
    df.columns = ['eventName', 'hit_timestamp',
                  'search_term', 'client_id_event', 'eventCount']
    df[['search_term', 'client_id_event']] = df[[
        'search_term', 'client_id_event']].astype(object)
    df['eventCount'] = df['eventCount'].astype(float)
    df['search_term'] = df.search_term.str.lower().str.strip()
    df['hit_timestamp'] = df.hit_timestamp.str.strip()
    df["hit_timestamp"] = df["hit_timestamp"].str.replace(
        '\+.*', '', regex=True)
    df["hit_timestamp"] = df["hit_timestamp"].str.replace(
        '-\d\d:.*', '', regex=True)
    df["hit_timestamp"] = df["hit_timestamp"].str.replace(
        '\..*', '', regex=True)
    df["date"] = pd.to_datetime(df["hit_timestamp"].str.replace(
        'T.*', '', regex=True), format='%Y-%m-%d')
    df["hit_timestamp"] = pd.to_datetime(
        df["hit_timestamp"], format='%Y-%m-%dT%H:%M:%S')
    df.insert(6, 'group', '')
    print(000)
    df = df.sort_values(by=['client_id_event', 'hit_timestamp'])
    print(111)

# перписать на плюс
    mask1 = df['eventName'] == df['eventName'].shift(1)
    mask2 = df['client_id_event'].eq(df['client_id_event'].shift(-1))
    mask3 = df['search_term'].astype(str).le(
        df['search_term'].shift(-1).astype(str))
    mask4 = df['hit_timestamp'].lt(df['hit_timestamp'].shift(-1))
    mask5 = (df['hit_timestamp'].shift(-1) - df['hit_timestamp']
             ).dt.total_seconds().div(60).lt(10)

    print(mask3)
    df['group'] = ~(mask3)

    df.loc[df.index[-1], 'group'] = True
    df.to_csv(
        f"C:/Users/User/Desktop/project/data/2ttttt_{file_name}.csv", index=False)


if __name__ == "__main__":
    df = pd.read_csv(f"{DATA_DIRECTORY}ed_default_search_term_july.csv")
    aggregate_search_terms(df, "search_term_july")
