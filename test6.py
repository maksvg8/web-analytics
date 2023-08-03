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
from custom_reports.modules.class_report import CustomReport

test = CustomReport('test','ed','test')
test.overwriting_old_csv_report(pivot_df)

unique_ids = df['id'].unique().tolist() 