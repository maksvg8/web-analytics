import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from custom_reports.modules.custom_reporting import *
from google_apis.sheets_api.modules.google_sheet_api import *
from config import (COAST_SHEET_ID, COAST_SHEET_RANGE, PLAN_SHEET_ID,
                    PLAN_SHEET_RANGE_JUNE, REPORT_SHEET_RANGE, FACT_SHEET_ID)
from credentials import DATA_DIRECTORY

def extract_cost_data_for_last_date(cost_data):
    if cost_data.empty == False:
        cost_data['Day'] = pd.to_datetime(cost_data['Day'])
        end_date = cost_data['Day'].min()
        last_cost_data = cost_data[cost_data['Day'] == end_date].copy()
        last_cost_data["Day"] = last_cost_data["Day"].astype(str)
        last_cost_data = last_cost_data.reset_index(drop=True)
        return last_cost_data

def overwriting_csv(data, file_name, duplicates = ['Project','Source','Account Name','Campaign Name']):
    # if the method was called without arguments, then the values from the attributes are used
    try:
        old_data = pd.read_csv(f"{DATA_DIRECTORY}{file_name}.csv")
        data = pd.concat(
            [old_data, data]).drop_duplicates(subset=duplicates)
        data.to_csv(f"{DATA_DIRECTORY}{file_name}.csv",
                                        index=False)
    except:
        data.to_csv(f"{DATA_DIRECTORY}{file_name}.csv",
                                        index=False)
    print("successful add data to csv")
    return data

if __name__ == '__main__':
    cost_data = get_rows_from_gooogle_sheets(COAST_SHEET_ID, COAST_SHEET_RANGE)
    last_cost = extract_cost_data_for_last_date(cost_data)
    print(last_cost)
    overwriting_csv(last_cost, 'test_test')