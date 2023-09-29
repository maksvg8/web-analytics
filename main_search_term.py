from google_apis.data_api.modules import ga4_reporting_v1 as ga4
from google_apis.data_api.config.default_configuration import (ga4_dim_search_term, ga4_metr_search_term)
from custom_reports.modules.search_term import aggregate_search_terms

report = ga4.GA4Report("search_term", "ED")
report.at_start_date = "2023-08-01"
report.at_end_date = "2023-08-31"
report.at_ga4_dim_list = ga4_dim_search_term
report.at_ga4_metr_list = ga4_metr_search_term
report.at_offset = 0
report.at_limit = 100000

report.set_filter('search_term')
df = report.ga4_all_rows_to_df()
print(df)
aggregate_search_terms(df, report.at_report_name)