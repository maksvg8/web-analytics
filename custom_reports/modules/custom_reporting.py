import pandas as pd
from datetime import timedelta, datetime
import re
from credentials import DATA_DIRECTORY
from custom_reports.config.default_configuration import sourcePatterns
from config import (BANNER_SHEET_ID ,BANNER_SHEET_ED_RANGE, BANNER_SHEET_EM_RANGE, BANNER_REPORT_SHEET_RANGE)


def extract_cost_data_for_last_date(cost_data):
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


def merge_ym_df_and_costs_data(dfYmDataED, dfYmDataEM, costData):
    columnsForYM = [
        'Date', 'UTMCapaigne', 'Visits', 'Users', 'Purchases', 'Revenue',
        'Registration'
    ]
    dfYmDataED.columns = columnsForYM
    dfYmDataEM.columns = columnsForYM
    dfADSData = convert_cost_colomns(costData)
    dfYmDataED['ProjectYM'] = 'ED'
    dfYmDataEM['ProjectYM'] = 'EM'
    concatenated_ym_df = pd.concat([dfYmDataED, dfYmDataEM], ignore_index=True)
    # concatenated_ym_df = concatenated_ym_df.drop(['Источник трафика (детально)', 'Источник трафика', 'UTM Source', 'UTM Medium'], axis=1)
    # agg_dict = {'Визиты': 'sum', 'Посетители': 'sum', 'Количество покупок' : 'sum', 'Доход, BYN': 'sum', 'Достижения цели (sign_up)': 'sum'}
    # agg_list = ['ProjectYM', 'Дата визита', 'UTM Campaign']
    # concatenated_ym_df = concatenated_ym_df.groupby(agg_list, as_index=False, sort=False).agg(agg_dict)
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



def set_project(project):
    if project == 'ed':
        sheet_range = BANNER_SHEET_ED_RANGE
        re_banner_parameter = '.*(ed_ban.*)'
        ...
    elif project == 'em':
        sheet_range = BANNER_SHEET_EM_RANGE
        re_banner_parameter = '.*(em_ban.*)'
        ...
    else:
        raise ValueError("Invalid project name")
    return sheet_range, re_banner_parameter


def extraction_banner_parameter(df, re_banner_parameter):
    df['Итоговая ссылка с меткой'] = df['Итоговая ссылка с меткой'].str.replace(rf'{re_banner_parameter}', r'\1', regex=True)
    return df


def transform_banner_data(df, PLACEMENT_START_ERROR = 0, PLACEMENT_END_ERROR = 0):
    '''
    Преобразует таблицу с отчетность по размещению баннеров в удобную для объединения с данными метрики.
    Использует коэфициент ошибки, если установить 1, будет отнимать 1 день от нрачала размещения и добавлять 1 день к концу размещения, по умолчаю 0.
    
    '''
    df = df.drop(df[df['Итоговая ссылка с меткой'] == "Ошибка: Есть незаполненное поле"].index)
    df['Дата начала размещения'] = pd.to_datetime(df['Дата начала размещения'], format="%d.%m.%Y") - timedelta(days=PLACEMENT_START_ERROR)
    df['Дата окончания размещения'] = pd.to_datetime(df['Дата окончания размещения'], format="%d.%m.%Y") + timedelta(days=PLACEMENT_END_ERROR)
    processedBudgetTable = []
    for _, row in df.iterrows():
        str_categ = row['Где размещается (или ID категории)']
        if str_categ == 'Весь каталог':
            str_categ = r'/categ.*'
        elif str_categ == 'Главная':
            str_categ = r'/'
        else:
            str_categ = str_categ.replace('_', '|')
            str_categ = rf'.*({str_categ}).*'
        row['Где размещается (или ID категории)'] = str_categ
        dates = pd.date_range(start=row['Дата начала размещения'], end=row['Дата окончания размещения'], freq='D')
        for date in dates:
            newRow = row.copy()
            newRow['Date'] = date
            processedBudgetTable.append(newRow)
        print(str_categ)
    new_df = pd.DataFrame(processedBudgetTable)
    ...
    return new_df




def get_date_range_from_banners_sheet(df, PLACEMENT_ERROR = 0):
    '''
    Использует коэфициент ошибки, если установить 1, будет отнимать 1 день от нрачала размещения и добавлять 1 день к концу размещения, по умолчаю 0.
    
    '''
    start_date = (df['Дата начала размещения'].min() - timedelta(days=PLACEMENT_ERROR)).strftime('%Y-%m-%d')
    end_date = (df['Дата окончания размещения'].max() + timedelta(days=PLACEMENT_ERROR)).strftime('%Y-%m-%d')
    ...
    return df, start_date, end_date


