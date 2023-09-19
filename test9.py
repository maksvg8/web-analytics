import pandas as pd

data = {
    'eventName': ['event1', 'event1', 'event1', 'event1', 'event1', 'event1', 'event1'],
    'client_id_event': [1, 2, 3, 4, 5, 6, 7],
    'search_term': ['apple', 'banana', 'apple', 'appleeeee', 'bike', 'car', 'dog'],
    'hit_timestamp': [
        '2023-08-16 10:00:00',
        '2023-08-16 10:00:00',
        '2023-08-16 10:00:00',
        '2023-08-16 10:00:00',
        '2023-08-16 10:00:00',
        '2023-08-16 10:00:00',
        '2023-08-16 10:00:00'
    ]
}

df = pd.DataFrame(data)

# Преобразуем столбец hit_timestamp в формат datetime
df['hit_timestamp'] = pd.to_datetime(df['hit_timestamp'])

# Отсортируем DataFrame по client_id_event и hit_timestamp
df = df.sort_values(by=['client_id_event', 'hit_timestamp'])

print(df)

# Определите условия
# mask1 = df['eventName'] == df['eventName'].shift(-1)
# mask2 = df['client_id_event'] == df['client_id_event'].shift(-1)
# mask3 = df['search_term'].astype(str).ge(df['search_term'].shift(-1).astype(str))
# mask4 = df['hit_timestamp'] < df['hit_timestamp'].shift(-1)
# mask5 = (df['hit_timestamp'].shift(-1) - df['hit_timestamp']).dt.total_seconds() / 60 < 10

# Создайте условие для обновления столбца 'group'
# df['group'] = ~(mask1 & mask2 & mask3 & mask4 & mask5)
# df['group'] = ~(mask3)
# Убедитесь, что последняя строка в группе устанавливается в True
# df['group'] = df.groupby('client_id_event')['group'].transform('ffill')

# Вывод обновленного DataFrame




# apply the function to each row in the DataFrame
df['group'] = df['client_id_event']
print(df)



import pandas as pd

# Создаем пример DataFrame
data = {
    'A': ['aaaa', 'en', 'end'],
    'B': ['aaaasa', 'end', 'red']
}

df = pd.DataFrame(data)

# Выбираем две строки (например, первую и вторую) и столбцы A и B
def contains_partial(a, b):
    return a in b

# Применяем функцию к DataFrame
# Выводим результат
print(df)


