from google_apis.data_api.modules import ga4_reporting_v1 as ga4
import pandas as pd
from google_apis.data_api.config.default_configuration import (ga4_dim_transaction_email, ga4_metr_transaction_email)


def email_report(report_name: str, project: str, start_date: str, end_date: str):
    report = ga4.GA4Report(report_name, project)
    report.at_start_date = start_date
    report.at_end_date = end_date
    report.at_ga4_dim_list = ga4_dim_transaction_email
    report.at_ga4_metr_list = ga4_metr_transaction_email
    report.at_offset = 0
    report.at_limit = 100000

    report.set_filter("email")
    df = report.ga4_all_rows_to_df()
    report.overwriting_old_csv_report()

if __name__ == '__main__':
    report_name = 'ga4_email_oct'
    projects = ['ED', 'EM']
    start_date = "2023-10-01"
    end_date = "2023-10-31"
    for project in projects:
        email_report(report_name, project, start_date, end_date)