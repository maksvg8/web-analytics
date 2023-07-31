import pandas as pd

# Создаем датафрейм с данными
data = {
    'date': ['2023-07-22', '2023-07-20', '2023-07-24', '2023-07-25', '2023-07-26'],
    'event_name': ['click', 'click', 'search', 'search', 'click'],
    'clid': [101, 102, 101, 103, 104],
    'total_events': [5, 5, 0, 2, 10]
}

df = pd.DataFrame(data)



# Фильтруем строки по условиям
filtered_df = df.loc[
    ~df['clid'].isin(
        df.loc[df['event_name'] == 'click', 'clid']
    )
]
print(filtered_df)

# Создание датафрейма исключений
# Отчет по запросам ботов
# создание листа с куками ботов
# Запись датафрейма исключений в csv




# # Группируем по clid и проверяем, есть ли событие "search" для каждого clid
# grouped = df.groupby('clid')['event_name'].apply(lambda x: 'click' not in x.values)
# print(grouped)

# # Фильтруем только те clid, у которых нет события "search"
# filtered_clid = grouped[grouped].index.tolist()
# print(filtered_clid)

# # Отбираем строки с отфильтрованными clid
# filtered_df = df[df['clid'].isin(filtered_clid)]

# print(filtered_df)
