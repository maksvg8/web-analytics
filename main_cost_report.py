import pandas as pd
import datetime
from yandex_apis.ym_reporting_api.modules import ym_reporting_api as ym
from custom_reports.modules.campaign_reporting import *
from custom_reports.modules.class_report import *
from google_apis.sheets_api.modules.google_sheet_api import *
from credentials import DATA_DIRECTORY
from config import (
    COAST_SHEET_ID,
    COAST_SHEET_RANGE,
    PLAN_SHEET_ID,
    PLAN_SHEET_RANGE_JUNE,
    PLAN_SHEET_RANGE_JULY,
    PLAN_SHEET_RANGE_AUGUST,
    REPORT_SHEET_RANGE,
)


def cost_report():
    cost_data = get_rows_from_gooogle_sheets(COAST_SHEET_ID, COAST_SHEET_RANGE)
    if cost_data.empty == True:
        start_date = datetime.date.today() - datetime.timedelta(days=60)
    else:
        backup_data = cost_data.copy(deep=True)
        last_cost_data = extract_cost_data_for_last_date(backup_data)
        for_last_cost_date = CustomReport("old_cost_data")
        for_last_cost_date.overwriting_old_csv_report(
            last_cost_data,
            "old_cost_data",
            True,
            ["Day", "Project", "Source", "Account Name", "Campaign Name"],
        )
        cost_data = cost_data[
            (cost_data["Project"] != "GS") & (cost_data["Project"] != "EU")
        ]
        date_definitions = cost_data.copy(deep=True)
        date_definitions["Day"] = pd.to_datetime(date_definitions["Day"])
        start_date = date_definitions["Day"].min()
    start_date = start_date.strftime("%Y-%m-%d")

    report_ed = ym.YandexMetricReport("ym_main_cost", "ED", "campaign_report")
    report_ed.at_start_date = start_date
    report_ed.at_project_name
    data_ed = report_ed.all_ym_rows_to_df()
    data_ed = transform_ym_ed_em_campaign_dfs(data_ed, report_ed.at_project_name)

    report_em = ym.YandexMetricReport("ym_main_cost", "EM", "campaign_report")
    report_em.at_start_date = start_date
    data_em = report_em.all_ym_rows_to_df()
    data_em = transform_ym_ed_em_campaign_dfs(data_em, report_em.at_project_name)

    report_jb = ym.YandexMetricReport("ym_main_cost", "JB", "campaign_report")
    report_jb.at_start_date = start_date
    data_jb = report_jb.all_ym_rows_to_df()
    data_jb = transform_ym_jb_campaign_df(data_jb)

    data_ed, data_em, data_jb = rename_campaign_df(data_ed, data_em, data_jb)
    concatenated_ym_df = concat_ym_campaign_dfs(data_ed, data_em, data_jb)
    merged_df = merge_ym_capaigne_df_and_costs_data(concatenated_ym_df, cost_data)

    # Получение данных бюджета
    plan_date_june = get_rows_from_gooogle_sheets(PLAN_SHEET_ID, PLAN_SHEET_RANGE_JUNE)
    plan_date_july = get_rows_from_gooogle_sheets(PLAN_SHEET_ID, PLAN_SHEET_RANGE_JULY)
    plan_date_august = get_rows_from_gooogle_sheets(
        PLAN_SHEET_ID, PLAN_SHEET_RANGE_AUGUST
    )

    # Преобразование бюджетов для последующего объединения
    plan_df_june = transform_planned_budget_df(
        plan_date_june, "2023-06-01", "2023-06-30"
    )
    plan_df_july = transform_planned_budget_df(
        plan_date_july, "2023-07-01", "2023-07-31"
    )
    plan_df_august = transform_planned_budget_df(
        plan_date_august, "2023-08-01", "2023-08-31"
    )
    concatenated_plan_df = pd.concat(
        [plan_df_june, plan_df_july, plan_df_august], ignore_index=True
    )

    # Финальное объединение
    final_df = merge_budget_and_costs_data(merged_df, concatenated_plan_df)

    # Подготовка к загрузке в гугл таблицы
    final_df = final_df.fillna("")
    delete_old_gooogle_sheet(COAST_SHEET_ID, REPORT_SHEET_RANGE)
    set_df_to_gooogle_sheets(COAST_SHEET_ID, REPORT_SHEET_RANGE, final_df)
    print('Main cost report complete')

if __name__ == "__main__":
    cost_report()
