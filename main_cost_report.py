import pandas as pd
from datetime import timedelta, datetime
from yandex_apis.ym_reporting_api.modules import ym_reporting_api as ym
from custom_reports.modules.custom_reporting import *
from google_apis.sheets_api.modules.google_sheet_api import *
from credentials import DATA_DIRECTORY
from config import (COAST_SHEET_ID, COAST_SHEET_RANGE, PLAN_SHEET_ID, PLAN_SHEET_RANGE_JUNE, PLAN_SHEET_RANGE_JULY, PLAN_SHEET_RANGE_AUGUST, REPORT_SHEET_RANGE)

def cost_report():
    cost_data = get_rows_from_gooogle_sheets(COAST_SHEET_ID, COAST_SHEET_RANGE)
    if cost_data.empty == True:
        start_date = datetime.date.today() - timedelta(days=60)
    else:
        backup_data = cost_data.copy(deep=True)
        last_cost_data = extract_cost_data_for_last_date(backup_data)
        overwriting_csv(last_cost_data, 'old_cost_data')
        cost_data = cost_data[(cost_data['Project'] != 'GS')&(cost_data['Project'] != 'EU')]
        date_definitions = cost_data.copy(deep=True)
        date_definitions['Day'] = pd.to_datetime(date_definitions['Day'])
        start_date = date_definitions['Day'].min()
    start_date = start_date.strftime('%Y-%m-%d')
    

    report_ed = ym.YandexMetricReport('ym_test', 'ed', 'campaign_report')
    report_ed.at_start_date = start_date
    data_ed = report_ed.all_ym_rows_to_df()

    report_em = ym.YandexMetricReport('ym_test', 'em', 'campaign_report')
    report_em.at_start_date = start_date
    data_em = report_em.all_ym_rows_to_df()

    merged_df = merge_ym_df_and_costs_data(data_ed, data_em, cost_data)

    # Получение данных бюджета
    plan_date_june = get_rows_from_gooogle_sheets(PLAN_SHEET_ID, PLAN_SHEET_RANGE_JUNE)
    plan_date_july = get_rows_from_gooogle_sheets(PLAN_SHEET_ID, PLAN_SHEET_RANGE_JULY)
    plan_date_august = get_rows_from_gooogle_sheets(PLAN_SHEET_ID, PLAN_SHEET_RANGE_AUGUST)

    # Преобразование бюджетов для последующего объединения
    plan_df_june = transform_planned_budget_df(plan_date_june, '2023-06-01', '2023-06-30')
    plan_df_july = transform_planned_budget_df(plan_date_july, '2023-07-01', '2023-07-31')
    plan_df_august = transform_planned_budget_df(plan_date_august, '2023-08-01', '2023-08-31')
    concatenated_plan_df = pd.concat([plan_df_june, plan_df_july, plan_df_august], ignore_index=True)

    # Финальное объединение
    final_df = merge_budget_and_costs_data(merged_df, concatenated_plan_df)

    # Подготовка к загрузке в гугл таблицы
    final_df = final_df.fillna('')
    delete_old_gooogle_sheet(COAST_SHEET_ID, REPORT_SHEET_RANGE)
    set_df_to_gooogle_sheets(COAST_SHEET_ID, REPORT_SHEET_RANGE, final_df)
    print(111)
    
if __name__ == "__main__":
    cost_report()