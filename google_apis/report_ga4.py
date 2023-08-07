from google_apis.data_api.modules import ga4_reporting_v1 as ga4
import pandas as pd
from google_apis.data_api.config.default_configuration import (ga4_dim_banners, ga4_metr_banners, ga4_dim_transaction,
                    ga4_metr_transaction, ga4_dim_ed_search,
                    ga4_metr_ed_search, ga4_dim_funnel, ga4_metr_funnel,
                    ga4_dim_List, ga4_metr_List, ga4_dim_transaction_email,
                    ga4_metr_transaction_email, ga4_dim_sessionManualTerm,
                    ga4_metr_sessionManualTerm,ga4_dim_search_term,ga4_metr_search_term,ga4_dim_custom,ga4_metr_custom)
from search_term import aggregate_search_terms

# report = ga4.GA4Report("search_term_july", "ed")
report = ga4.GA4Report("ga4_mail_july", "em")
report.at_start_date = "2023-07-01"
report.at_end_date = "2023-07-31"
# report.at_ga4_dim_list = ga4_dim_search_term
# report.at_ga4_metr_list = ga4_metr_search_term
report.at_ga4_dim_list = ga4_dim_transaction_email
report.at_ga4_metr_list = ga4_metr_transaction_email
# report.at_ga4_dim_list = ga4_dim_transaction
# report.at_ga4_metr_list = ga4_metr_transaction
# report.at_ga4_dim_list = ga4_dim_sessionManualTerm
# report.at_ga4_metr_list = ga4_metr_sessionManualTerm
# # report.at_ga4_dim_list = ga4_dim_custom
# # report.at_ga4_metr_list = ga4_metr_custom
# report.at_ga4_dim_list = ga4_dim_banners
# report.at_ga4_metr_list = ga4_metr_banners
report.at_offset = 0
report.at_limit = 100000

df = report.ga4_all_rows_to_df()
report.overwriting_old_csv_report()

# df = df.reset_index(drop=True)
# aggregate_search_terms(df, report.at_report_name)



# нужно переписать логику поиска файла по имени (нужно использовать имя проекта и имя )