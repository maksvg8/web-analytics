from google_apis.data_api.modules import ga4_reporting_v1 as ga4
from google_apis.data_api.config.default_configuration import (ga4_dim_search_term, ga4_metr_search_term)
from custom_reports.modules.search_term import aggregate_search_terms

report_name = input("Введите имя отчета, пример serch_term_september: ")
report = ga4.GA4Report(report_name, "ED")
report.at_start_date = input("Введите дату начала отчета, пример 2023-09-01: ")
report.at_end_date = input("Введите дату окончания отчета, пример 2023-09-30: ")
report.at_ga4_dim_list = ga4_dim_search_term
report.at_ga4_metr_list = ga4_metr_search_term
report.at_offset = 0
report.at_limit = 100000

report.set_filter('search_term')
df = report.ga4_all_rows_to_df()
report.overwriting_old_csv_report()
print(df)
aggregate_search_terms(df, report.at_report_name)