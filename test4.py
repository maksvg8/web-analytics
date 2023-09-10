import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from custom_reports.modules.custom_reporting import *
from google_apis.sheets_api.modules.google_sheet_api import *
from config import (COAST_SHEET_ID, COAST_SHEET_RANGE, PLAN_SHEET_ID,
                    PLAN_SHEET_RANGE_JUNE, REPORT_SHEET_RANGE, FACT_SHEET_ID)

def test_df():
    report_data = extract_rows_from_gooogle_sheets(COAST_SHEET_ID, REPORT_SHEET_RANGE)
    if report_data.empty == False:
        report_data['Date'] = pd.to_datetime(report_data['Date'])
        start_date = report_data['Date'].min()
        start_date = start_date.strftime('%Y-%m-%d')
        end_date = datetime.today()- timedelta(days=1)
        end_date = end_date.strftime('%Y-%m-%d')
    else:
        start_date = pd.to_datetime('2023-05-01')
        end_date = pd.to_datetime('2023-06-30')

    report_data["Date"] = pd.to_datetime(report_data["Date"])
    report_data = report_data[(report_data['Date'] >= start_date)&(report_data['Date'] <= end_date)&((report_data['Project'] == "EM"))]
    # |(report_data['Project'] == "EM")

    report_data = report_data.drop(['UTMCapaigne', 'Account Name','Source', 'Account Currency',
        'Direction', 'Visits','Users', 'Registration', 'Daily Budget', 'Clicks',
        'Impressions','Budget'], axis=1)
    group_columns = [
        'Date','Project'
    ]
    sum_columns = [
        'Purchases', 'Revenue',   'Cost'
    ]
    report_data[sum_columns] = report_data[sum_columns].replace(',', '.', regex=True).astype(float)
    grouped_df = report_data.groupby(group_columns, as_index=False, sort=False, dropna=False).agg('sum')
    df_reindexed = grouped_df.reindex(columns=[
        'Date','Project', 'Purchases', 'Revenue', 'Cost'
    ])
    df_reindexed = df_reindexed.drop(['Project'], axis=1)
    print(df_reindexed)

    input_data = df_reindexed.copy()
    input_data.set_index('Date', inplace=True)
    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(10, 15))
    for i, column in enumerate(input_data.columns):
        ax = input_data[column].plot(ax=axes[i], title=column, legend=True, color='b', label='Данные')
        input_data[column].plot(ax=ax, legend=True, color='r', label='Прогноз')
        ax.set_xlabel('Дата')
        ax.set_ylabel('Значение')
        
        # Форматируем значения оси Y в более понятный вид (без научной нотации) только для столбца 'Доход'
        if column == 'Доход':
            formatter = ticker.FuncFormatter(lambda x, p: f'{x/1e6:.0f} млн')
            ax.yaxis.set_major_formatter(formatter)
        
        ax.legend()

    plt.tight_layout()
    plt.show()

    # df_reindexed.to_excel("df_reindexed.xlsx", index=False)
    return df_reindexed

