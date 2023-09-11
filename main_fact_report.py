import pandas as pd
from custom_reports.modules.custom_reporting import *
from google_apis.sheets_api.modules.google_sheet_api import *
from config import (COAST_SHEET_ID, COAST_SHEET_RANGE, PLAN_SHEET_ID,
                    PLAN_SHEET_RANGE_JUNE, REPORT_SHEET_RANGE, FACT_SHEET_ID)

def fact_report(start_date, end_date):
    report_data = extract_rows_from_gooogle_sheets(COAST_SHEET_ID, REPORT_SHEET_RANGE)
    report_data["Date"] = pd.to_datetime(report_data["Date"])
    report_data = report_data[(report_data['Date'] >= start_date)&(report_data['Date'] <= end_date)]

    report_data = report_data.drop(['Date','Account Name'], axis=1)
    group_columns = [
        'UTMCapaigne', 'Project', 'Source', 'Account Currency',
        'Direction', 'Daily Budget'
    ]
    sum_columns = [
        'Visits','Users', 'Purchases', 'Revenue', 'Registration', 'Goal', 'Clicks', 'Cost',
        'Impressions', 'Budget'
    ]
    report_data[sum_columns] = report_data[sum_columns].replace(',', '.', regex=True).astype(float)
    grouped_df = report_data.groupby(group_columns, as_index=False, sort=False, dropna=False).agg('sum')
    df_reindexed = grouped_df.reindex(columns=[
        'Project', 'Source', 'Direction', 'UTMCapaigne',
        'Account Currency', 'Visits','Users', 'Purchases', 'Revenue', 'Registration', 'Goal',
        'Clicks', 'Impressions', 'Daily Budget', 'Budget', 'Cost'
    ])
    df_reindexed = df_reindexed.fillna('')
    clear_old_gooogle_sheet(FACT_SHEET_ID, "'Факт Август'!A1:P")
    add_df_to_gooogle_sheets(FACT_SHEET_ID, "'Факт Август'!A1:P", df_reindexed)


if __name__ == '__main__':
    start_date = pd.to_datetime('2023-08-01')
    end_date = pd.to_datetime('2023-08-31')
    fact_report(start_date, end_date)