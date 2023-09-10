import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

july = pd.read_csv('C:/Users/User/Desktop/project/data/agg2_search_term_july.csv')

july.loc[(july['eventName'] == 'search_complete') | (july['eventName'] == 'search'), 'eventName'] = 'view'
july.loc[(july['eventName'] == 'search_complete_select') | (july['eventName'] == 'search_select'), 'eventName'] = 'click'
# july = july.drop(['search_term', 'date', 'eventCount', 'hit_timestamp'], axis=1)
print(july.head())
# Загрузка исходных данных

# # Группировка данных по запросу и дате
# grouped_data = july.groupby(['date', 'search_term'])

# # Вычисление CTR для каждой группы
# grouped_data['CTR'] = (grouped_data['eventName'].eq('click').sum() / grouped_data['всего событий'].eq('view').sum()) * 100

# # Создание нового DataFrame с результатами
# ctr_data = grouped_data.reset_index()

# # Вывод результатов
# print(ctr_data)


# Создание группировок для событий "клик" и "просмотр"
click_group = july[july['eventName'] == 'click'].groupby(['date', 'search_term'])
view_group = july[july['eventName'] == 'view'].groupby(['date', 'search_term'])
clients = july.groupby(['date', 'search_term'])['client_id_event'].sum()

# Вычисление CTR
click_count = click_group['client_id_event'].sum()
view_count = view_group['client_id_event'].sum()
ctr_series = (click_count / view_count) * 100

# Создание нового DataFrame с результатами CTR
ctr_df = pd.DataFrame( {'CTR': ctr_series, 'users': clients})
# ctr_df = ctr_df.drop(['search_term','date'], axis=1)
ctr_df = ctr_df.dropna(subset=['CTR', 'users'])
print(ctr_df.info())
print(ctr_df.describe())
print(ctr_df.head())



plt.figure(figsize=(10, 6))
plt.hist(ctr_df['CTR'], bins=20, color='c', edgecolor='k')
plt.title('Гистограмма CTR')
plt.xlabel('CTR')
plt.ylabel('Частота')
plt.grid(True)
plt.tight_layout()
plt.show()


# Создание точечного графика
plt.figure(figsize=(10, 6))
plt.scatter( ctr_df['CTR'], ctr_df['users'], alpha=0.5)
plt.title('CTR по количеству пользователей')
plt.xlabel('Количество пользователей')
plt.ylabel('CTR')
plt.grid(True)
plt.xlim(0.0, 200.0)  # Установите нужные пределы на оси X
# plt.ylim(0.0, 1000.0) # Установите нужные пределы на оси Y
plt.tight_layout()
plt.show()


# plt.figure(figsize=(10, 6))
# plt.hist2d(ctr_df['users'], ctr_df['CTR'], bins=(10, 20), cmap=plt.cm.YlGnBu)
# plt.colorbar(label='Частота')
# plt.title('Гистограмма CTR по числу пользователей')
# plt.xlabel('CTR')
# plt.ylabel('Число пользователей')
# plt.grid(True)
# plt.tight_layout()
# plt.show()


# plt.figure(figsize=(10, 6))
# plt.hist(ctr_df[['users','CTR']], bins=20, alpha=0.9)
# plt.title('Гистограмма CTR по числу пользователей')
# plt.xlabel('CTR')
# plt.ylabel('Число пользователей')
# plt.grid(True)
# plt.tight_layout()
# plt.show()