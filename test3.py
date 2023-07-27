import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from statsmodels.tsa.vector_ar.var_model import VAR
from test4 import *

# Исходные данные
data = {
    'Date': pd.date_range(start='2022-10', periods=9, freq='M'),
    'Количество заказов': [126378, 107643, 110609, 104653, 96727, 90115, 75217, 81025, 70680],
    'Доход': [7747992, 6347791, 6947980, 6337190, 6207115, 5849629, 5022846, 5378287, 4853560],
    'Количество посетителей': [365637, 355370, 324399, 291388, 288130, 294920, 288007, 282672, 239013],
    'Выручка с клиента': [21, 18, 21, 22, 22, 20, 17, 19, 20],
    'Средний чек': [61, 59, 63, 61, 64, 65, 67, 66, 69]
}

# Create DataFrame from the data
df1 = pd.DataFrame(data)
df1 = test_df()
df = df1.copy()

df.set_index('Date', inplace=True)

# Прогноз для всех временных рядов (мультивариативный прогноз)
forecast_periods = 5

input_data = df.copy()

# Функция для прогнозирования мультивариативной модели VAR
def forecast_VAR(data, forecast_periods):
    model = VAR(data)
    model_fit = model.fit()
    forecast = model_fit.forecast(model_fit.endog, steps=forecast_periods)
    return forecast

# Initialize forecast_values DataFrame to store the forecasted values
forecast_values = pd.DataFrame(index=pd.date_range(start='2023-07-27', periods=forecast_periods, freq='D'))

for column in input_data.columns:
    forecast = forecast_VAR(input_data, forecast_periods=forecast_periods)
    forecast_values[column] = forecast[:, input_data.columns.get_loc(column)]
    # Update input_data with the forecasted values for subsequent iterations
    input_data[column][-forecast_periods:] = forecast[:, input_data.columns.get_loc(column)]

# Объединим исходные данные и прогнозные значения
forecast_df = pd.concat([df, forecast_values])

# Построим графики для прогнозных значений
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(10, 15))
for i, column in enumerate(forecast_df.columns):
    ax = forecast_df[column].plot(ax=axes[i], title=column, legend=True, color='b', label='Данные')
    forecast_values[column].plot(ax=ax, legend=True, color='r', label='Прогноз')
    ax.set_xlabel('Дата')
    ax.set_ylabel('Значение')
    
    # Форматируем значения оси Y в более понятный вид (без научной нотации) только для столбца 'Доход'
    if column == 'Доход':
        formatter = ticker.FuncFormatter(lambda x, p: f'{x/1e6:.0f} млн')
        ax.yaxis.set_major_formatter(formatter)
    
    ax.legend()

plt.tight_layout()
plt.show()

# Создадим новый датафрейм для всех значений
all_values_df = forecast_df.copy()

# Выведем результаты в консоль
print(all_values_df)