import pandas as pd

# Создаем датафрейм с данными
data = {
    'url': ['example.com/page1', 'example.com/page2', 'example.com/page3', 'other.com/4'],
    'value': [10, 10, 10, 10]
}

df = pd.DataFrame(data)

# Определите регулярное выражение
str_categ = r'.*page.*'

# Используйте str.extract() для получения совпадающих групп
filtered_df = df[(df['url'].str.extract(str_categ, expand=False).notnull()) &(df['value'] >= 20)]

# Суммируем значения столбца 'value'
total_value = filtered_df['value'].sum()

print(filtered_df)
print("Total value:", total_value)