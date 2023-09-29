import pandas as pd
import numpy as np
import datetime
import re
from credentials import DATA_DIRECTORY
from custom_reports.config.default_configuration import sourcePatterns


def extract_cost_data_for_last_date(cost_data):
    cost_data['Day'] = pd.to_datetime(cost_data['Day'])
    start_date = cost_data['Day'].min()
    end_date = cost_data['Day'].min() + datetime.timedelta(days=14)
    last_cost_data = cost_data[(cost_data['Day'] >= start_date)&(cost_data['Day'] <= end_date)].copy()
    last_cost_data["Day"] = last_cost_data["Day"].astype(str)
    last_cost_data = last_cost_data.reset_index(drop=True)
    return last_cost_data


def set_source_from_utm(df, sourceColumn, campaignColumn):
    sourceColumn = str(sourceColumn)
    campaignColumn = str(campaignColumn)
    for index, row in df.iterrows():
        if pd.isna(row[sourceColumn]):
            for key, value in sourcePatterns.items():
                if re.match(rf"{value}", str(row[campaignColumn])):
                    df.loc[index, sourceColumn] = key
                    break
            else:
                df.loc[index, sourceColumn] = "Other Sources"
    return df


def convert_cost_colomns(df):
    columnsToConvert = ['Clicks', 'Cost', 'Impressions']
    df[columnsToConvert] = df[columnsToConvert].replace(
        ',', '.', regex=True).astype(float)
    return df


def convert_plan_colomns(df):
    columnsToConvert = ['Plan BYN c НДС']
    df[columnsToConvert] = df[columnsToConvert].replace(
        ',', '.', regex=True).astype(float)
    return df


def transform_ym_ed_em_campaign_dfs(df_ym_data_ed, project_name = 'ED'):
    df_ym_data_ed[['Goal','ProjectYM']] = 0, project_name
    return df_ym_data_ed


def transform_ym_jb_campaign_df(jb_df):
    jb_df[['Purchases','Revenue','Registration','ProjectYM']] = 0, 0, 0, 'JB'
    column_to_move = jb_df.pop('ym:s:goal223656836reaches')
    jb_df.insert(7, 'Goal', column_to_move)
    return jb_df

def rename_campaign_df(*dfs):
    columns_for_ed_em = [
        'Date', 'UTMCapaigne', 'Visits', 'Users', 'Purchases', 'Revenue',
        'Registration', 'Goal', 'ProjectYM'
    ]
    for df in dfs:
        df.columns = columns_for_ed_em
    return dfs

def concat_ym_campaign_dfs(df_ym_data_ed, df_ym_data_em, *other):
    concatenated_ym_df = pd.concat([df_ym_data_ed, df_ym_data_em, *other], ignore_index=True)
    return concatenated_ym_df


def merge_ym_capaigne_df_and_costs_data(concatenated_ym_df, costData):
    dfADSData = convert_cost_colomns(costData)
    mergedDF = pd.merge(concatenated_ym_df,
                        dfADSData,
                        left_on=['Date', 'UTMCapaigne'],
                        right_on=['Day', 'Campaign Name'],
                        how='outer')
    mergedDF['Date'].fillna(mergedDF['Day'], inplace=True)
    mergedDF['UTMCapaigne'].fillna(mergedDF['Campaign Name'], inplace=True)
    mergedDF['Project'].fillna(mergedDF['ProjectYM'], inplace=True)

    mergedDF = mergedDF.drop(
        ['Day', 'Campaign Name', 'ProjectYM', 'Campaign Status'], axis=1)
    mergedDF = set_source_from_utm(mergedDF, 'Source', 'UTMCapaigne')
    # mergedDF.to_excel(f"{dataDirectory}ym_and_cost_data.xlsx",
    #                   index=False)
    # mergedDF.to_csv(f"{dataDirectory}ym_and_cost_data.csv", index=False)
    return mergedDF


def transform_planned_budget_df(budgetDF, startDate, endDate):
    budgetDF = convert_plan_colomns(budgetDF)
    # Создание нового DataFrame с расширенными данными
    processedBudgetTable = []
    for _, row in budgetDF.iterrows():
        plan = row['Plan BYN c НДС']
        # Создание списка с датами в выбранном диапазоне
        dates = pd.date_range(start=startDate, end=endDate, freq='D')
        # Расчет стоимости на каждую дату
        try:
            daily_plan = round(plan / len(dates), 3)
        except:
            daily_plan = 0
        # Добавление строк с датами и расчитанной стоимостью в новый DataFrame
        for date in dates:
            newRow = row.copy()
            newRow['Date Budget'] = date
            newRow['Budget'] = daily_plan
            processedBudgetTable.append(newRow)
    newDF = pd.DataFrame(processedBudgetTable)
    newDF['Date Budget'] = newDF['Date Budget'].astype(str)
    newDF = newDF.drop(['Plan BYN c НДС'], axis=1)

    # new_df.to_excel(f"{dataDirectory}11111new_df.xlsx", index=False)
    # new_df.to_csv(f"{dataDirectory}11111new_df.csv", index=False)
    return newDF


def merge_budget_and_costs_data(mergedCostDF, transformedPlannedBudgetDF):
    finalDF = pd.merge(mergedCostDF,
                       transformedPlannedBudgetDF,
                       left_on=['Date', 'UTMCapaigne'],
                       right_on=['Date Budget', 'Plan UTM'],
                       how='outer')
    finalDF['Date'].fillna(finalDF['Date Budget'], inplace=True)
    finalDF['UTMCapaigne'].fillna(finalDF['Plan UTM'], inplace=True)
    finalDF['Source'].fillna(finalDF['Plan source'], inplace=True)
    finalDF['Project'].fillna(finalDF['Service'], inplace=True)
    finalDF['Account Currency'].fillna(finalDF['Currency'], inplace=True)
    finalDF = finalDF.drop(
        ['Date Budget', 'Plan UTM', 'Plan source', 'Service', 'Currency'],
        axis=1)
    ...
    return finalDF
