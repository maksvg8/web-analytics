import pandas as pd
from datetime import timedelta, datetime
from yandex_apis.ym_reporting_api.modules import ym_reporting_api as ym
from custom_reports.modules.custom_reporting import *
from google_apis.sheets_api.modules.google_sheet_api import *
from config import (BANNER_SHEET_ID ,BANNER_SHEET_ED_RANGE, BANNER_SHEET_EM_RANGE, BANNER_REPORT_SHEET_RANGE)


def banner_report(project):
    sheet_range, re_banner_parameter = set_project_for_banners(project)
    banners = get_rows_from_gooogle_sheets(BANNER_SHEET_ID, sheet_range)
    banners = transform_banners_sheet(banners)

    banners = extraction_banner_parameter(banners, re_banner_parameter)
    banners['Итоговая ссылка с меткой'] = banners['Итоговая ссылка с меткой'].str.replace(rf'{re_banner_parameter}', r'\1', regex=True)
    start_date, end_date = get_date_range_from_banners_sheet(banners)


    
    banner_click_data = ym.YandexMetricReport('banner', project, 'banner_report')
    banner_click_data.at_start_date = start_date
    banner_click_data.at_end_date = end_date
    banner_click_df = banner_click_data.all_ym_rows_to_df()


    banners['Date'] = banners['Date'].astype(str)
    banner_data_click = pd.merge(banners,
                       banner_click_df,
                       left_on=['Date', 'Итоговая ссылка с меткой'],
                       right_on=['ym:pv:date', 'ym:pv:URLParamNameAndValue'],
                       how='left')

    category_data = ym.YandexMetricReport('category', project, 'category_report')
    category_data.at_start_date = start_date
    category_data.at_end_date = end_date
    category_data_df = category_data.all_ym_rows_to_df()

    new_df = get_views_from_categories(banner_data_click, category_data_df)
    new_df.to_excel("df_3333333.xlsx", index=False)

    
    # if cost_data.empty == False:
    #     cost_data['Day'] = pd.to_datetime(cost_data['Day'])
    #     start_date = cost_data['Day'].min()
    # else:
    #     start_date = datetime.date.today() - timedelta(days=60)
    # start_date = start_date.strftime('%Y-%m-%d')
        

    # report_ed = ym.YandexMetricReport('banner', 'ed', 'banner_report')
    # report_ed.at_start_date = start_date
    # # reportED.atEndDate = '2023-06-18'
    # data_ed = report_ed.all_ym_rows_to_df()

    # report_em = ym.YandexMetricReport('banner', 'em', 'banner_report')
    # report_em.at_start_date = start_date
    # # reportEM.atEndDate = '2023-06-18'
    # data_em = report_em.all_ym_rows_to_df()

    # cost_data = get_rows_from_gooogle_sheets(COAST_SHEET_ID, COAST_SHEET_RANGE)
    # merged_df = merge_ym_df_and_costs_data(data_ed, data_em, cost_data)

    # # Получение данных бюджета
    # plan_date_june = get_rows_from_gooogle_sheets(PLAN_SHEET_ID, PLAN_SHEET_RANGE_JUNE)
    # plan_date_july = get_rows_from_gooogle_sheets(PLAN_SHEET_ID, PLAN_SHEET_RANGE_JULY)
    # plan_date_august = get_rows_from_gooogle_sheets(PLAN_SHEET_ID, PLAN_SHEET_RANGE_AUGUST)

    # # Преобразование бюджетов для последующего объединения
    # plan_df_june = transform_planned_budget_df(plan_date_june, '2023-06-01', '2023-06-30')
    # plan_df_july = transform_planned_budget_df(plan_date_july, '2023-07-01', '2023-07-31')
    # plan_df_august = transform_planned_budget_df(plan_date_august, '2023-08-01', '2023-08-31')
    # concatenated_plan_df = pd.concat([plan_df_june, plan_df_july, plan_df_august], ignore_index=True)

    # # Финальное объединение
    # final_df = merge_budget_and_costs_data(merged_df, concatenated_plan_df)

    # # Подготовка к загрузке в гугл таблицы
    # final_df = final_df.fillna('')
    # del_data = delete_old_gooogle_sheet(BANNER_SHEET_ID, BANNER_REPORT_SHEET_RANGE)
    # set_data = set_df_to_gooogle_sheets(BANNER_SHEET_ID, BANNER_REPORT_SHEET_RANGE, final_df)

    
if __name__ == "__main__":
    banner_report('ed')