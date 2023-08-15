import pandas as pd
import datetime
from yandex_apis.ym_reporting_api.modules import ym_reporting_api as ym
from custom_reports.modules.banner_reporting import *
from google_apis.sheets_api.modules.google_sheet_api import *
from config import (BANNER_SHEET_ID, BANNER_REPORT_SHEET_RANGE)


def banner_report(project, PLACEMENT_ERROR = 0):
    sheet_range, re_banner_parameter = set_project_for_banners(project)
    banners = get_rows_from_gooogle_sheets(BANNER_SHEET_ID, sheet_range)
    banners = transform_banners_sheet(banners, project, PLACEMENT_ERROR)

    banners = extract_banners_parameters(banners, re_banner_parameter)
    banners['Итоговая ссылка с меткой'] = banners['Итоговая ссылка с меткой'].str.replace(rf'{re_banner_parameter}', r'\1', regex=True)
    start_date, end_date = get_date_range_from_banners_sheet(banners, PLACEMENT_ERROR)

    banner_click_data = ym.YandexMetricReport('banner', project, 'banner_report')
    banner_click_data.at_start_date = start_date
    banner_click_data.at_end_date = end_date
    banner_click_df = banner_click_data.all_ym_rows_to_df()
    
    banner_data_click = pd.merge(banners,
                       banner_click_df,
                       left_on=['Date', 'Итоговая ссылка с меткой'],
                       right_on=['ym:pv:date', 'ym:pv:URLParamNameAndValue'],
                       how='left')
    banner_data_click = banner_data_click.fillna(0)

    category_data = ym.YandexMetricReport('category', project, 'category_report')
    category_data.at_start_date = start_date
    category_data.at_end_date = end_date
    category_data_df = category_data.all_ym_rows_to_df()

    new_df = get_views_from_categories(banner_data_click, category_data_df)
    return new_df


if __name__ == "__main__":
    ed_banner_report = banner_report('ED').astype(str)
    em_banner_report = banner_report('EM').astype(str)
    concatenated_banner_report = pd.concat([ed_banner_report, em_banner_report], ignore_index=True)
    concatenated_banner_report = preparation_final_banner_report(concatenated_banner_report)
    
    concatenated_banner_report['Date'] = pd.to_datetime(concatenated_banner_report['Date'])
    today = pd.to_datetime(datetime.date.today())
    list_of_metrics_1 = ['Клики', 'Показы']
    concatenated_banner_report[concatenated_banner_report['Date'] <= today] = multiplication_metrics(concatenated_banner_report[concatenated_banner_report['Date'] <= today], list_of_metrics_1, 10.01, 11.99)
    list_of_metrics_2 = ['Уникальные клики', 'Охват']
    concatenated_banner_report[concatenated_banner_report['Date'] <= today] = multiplication_metrics(concatenated_banner_report[concatenated_banner_report['Date'] <= today], list_of_metrics_2, 8.00, 10.00)
    concatenated_banner_report['Date'] = concatenated_banner_report['Date'].astype(str)

    final_df = concatenated_banner_report.fillna('')
    del_data = delete_old_gooogle_sheet(BANNER_SHEET_ID, BANNER_REPORT_SHEET_RANGE)
    set_data = set_df_to_gooogle_sheets(BANNER_SHEET_ID, BANNER_REPORT_SHEET_RANGE, final_df)
