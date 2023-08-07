import pandas as pd

data = {
    'user id': [1, 1, 2, 2, 3, 3],
    'eventName': ['A', 'B', 'A', 'B', 'A', 'B'],
    'eventName2': ['A', 'B', 'A', 'B', 'A', 'B'],
    'value': [10, 20, 30, 40, 50, 60]
}
df = pd.DataFrame(data)

# Транспонируем столбец 'eventName' и рассчитываем столбцы 'A' и 'B' для каждого 'user id'
pivot_df = df.pivot_table(index='user id', columns='eventName', values='value', aggfunc='sum', fill_value=0)
print(pivot_df)
# Переименовываем столбцы и суммируем значения для столбца 'eventName'
pivot_df.columns = ['A', 'B']
pivot_df['sum'] = pivot_df['A'] + pivot_df['B']
pivot_df = pivot_df.reset_index()
print(pivot_df)







import pandas as pd
import numpy as np

# Создаем пример датафрейма
data = {
    'values1': [5.1, 10.7, 15.3, 20.8, 25.5],
    'values2': [3.2, 7.6, 11.4, 16.2, 22.1]
}

df = pd.DataFrame(data)

# Генерируем случайные числа из заданного диапазона
random_factors = np.random.uniform(9.05, 11.13, size=(len(df), 2))

# Умножаем выбранные столбцы на случайные числа
df[['values1', 'values2']] = df[['values1', 'values2']] * random_factors

# Округляем выбранные столбцы до целых чисел
df[['values1', 'values2']] = df[['values1', 'values2']].round(0)

print(df)

lst = [3.2, 7.6, 11.4, 16.2, 22.1]
print(len(lst))