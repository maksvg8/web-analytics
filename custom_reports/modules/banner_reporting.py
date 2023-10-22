import pandas as pd
import numpy as np
import datetime
from config import (BANNER_SHEET_ED_RANGE, BANNER_SHEET_EM_RANGE)


def set_project_for_banners(project):
    if project == 'ED':
        sheet_range = BANNER_SHEET_ED_RANGE
        re_banner_parameter = '.*(ed_ban.*)'
        ...
    elif project == 'EM':
        sheet_range = BANNER_SHEET_EM_RANGE
        re_banner_parameter = '.*(em_ban.*)'
        ...
    else:
        raise ValueError("Invalid project name")
    return sheet_range, re_banner_parameter


def extract_banners_parameters(df, re_banner_parameter):
    df['Итоговая ссылка с меткой'] = df['Итоговая ссылка с меткой'].str.replace(rf'{re_banner_parameter}', r'\1', regex=True)
    return df



def transform_plan_date_columns(df, column_a, column_b):
    mask = df[column_a].notnull()
    df.loc[mask, column_b] = df[column_a]
    return df


def transform_fact_date_columns(df, column_a, column_b):
    mask = df[column_b].isnull()
    df.loc[mask, column_b] = df[column_a]
    return df


def transform_banners_sheet(df, project, PLACEMENT_ERROR = 0):
    '''
    Преобразует таблицу с отчетностью по размещению баннеров в удобную для объединения с данными метрики.
    Использует коэфициент ошибки, если установить 1, будет отнимать 1 день от нрачала размещения и добавлять 1 день к концу размещения
    
    '''
    df['Проект'] = project
    df = df.drop(df[df['Итоговая ссылка с меткой'] == "Ошибка: Есть незаполненное поле"].index)
    df['Реальная дата СТАРТА размещения'] = pd.to_datetime(df['Реальная дата СТАРТА размещения'], format="%d.%m.%Y") - datetime.timedelta(days=PLACEMENT_ERROR)
    df['Реальная дата КОНЦА размещения'] = pd.to_datetime(df['Реальная дата КОНЦА размещения'], format="%d.%m.%Y") + datetime.timedelta(days=PLACEMENT_ERROR)
    new_banners_sheet = []
    for _, row in df.iterrows():
        str_categ = row['Где размещается (или ID категории)']
        if str_categ == 'Весь каталог':
            str_categ = r'(/categ).*'
        elif str_categ == 'Главная':
            str_categ = r'(/)'
        else:
            str_categ = str_categ.replace('_', '|')
            str_categ = rf'.*({str_categ}).*'
        row['Где размещается (или ID категории)'] = str_categ
        dates = pd.date_range(start=row['Реальная дата СТАРТА размещения'], end=row['Реальная дата КОНЦА размещения'], freq='D')
        for date in dates:
            newRow = row.copy()
            newRow['Date'] = date
            new_banners_sheet.append(newRow)
    new_df = pd.DataFrame(new_banners_sheet)
    new_df['Date'] = new_df['Date'].astype(str)
    ...
    return new_df


def get_date_range_from_banners_sheet(df, PLACEMENT_ERROR = 0):
    '''
    Получает даты начала и конца для запросов к Яндекс метрике
    Использует коэфициент ошибки, если установить 1, будет отнимать 1 день от нрачала размещения и добавлять 1 день к концу размещения, по умолчаю 0.
    
    '''
    start_date = (df['Реальная дата СТАРТА размещения'].min() - datetime.timedelta(days=PLACEMENT_ERROR)).strftime('%Y-%m-%d')
    end_date = (df['Реальная дата КОНЦА размещения'].max() + datetime.timedelta(days=PLACEMENT_ERROR))
    today = pd.Timestamp.today()
    if end_date >= today:
        end_date = today.strftime('%Y-%m-%d')
    else:
        end_date = end_date.strftime('%Y-%m-%d')
        ...
    return start_date, end_date


def get_views_from_categories(banners_df, category_data_df):
    '''
    Суммрует просмотры категорий соответствующие шаблону регулярного выражения из таблицы банннеров

    '''
    new_banners_sheet = []
    for _, row in banners_df.iterrows():
        str_categ = row['Где размещается (или ID категории)']
        date_categ = row['Date']
        filtered_df = category_data_df[(category_data_df['ym:pv:URLPath'].str.extract(str_categ, expand=False).notnull()) & (category_data_df['ym:pv:date'] == date_categ)]
        total_value = filtered_df[['ym:pv:pageviews','ym:pv:users']].sum()
        new_row = row.copy()
        new_row['pageviews'] = total_value[0]
        new_row['users'] = total_value[1]
        new_banners_sheet.append(new_row)
    new_df = pd.DataFrame(new_banners_sheet)
    ...
    return new_df


def preparation_final_banner_report(banner_report_df):
    banner_report_df = banner_report_df.drop(['Где размещается (или ID категории)', 'ym:pv:date', 'ym:pv:URLParamNameAndValue', 'Дата старта в отчет', 'Дата окончания в отчет', 'Реальная дата СТАРТА размещения', 'Реальная дата КОНЦА размещения'], axis=1)
    new_columns = {'ym:pv:pageviews': 'Клики','ym:pv:users': 'Уникальные клики','pageviews': 'Показы','users': 'Охват'}
    banner_report_df = banner_report_df.rename(columns=new_columns)
    banner_report_df['Дата начала размещения'] = pd.to_datetime(banner_report_df['Дата начала размещения'], format="%d.%m.%Y")
    banner_report_df['Дата окончания размещения'] = pd.to_datetime(banner_report_df['Дата окончания размещения'], format="%d.%m.%Y")
    banner_report_df[['Дата начала размещения','Дата окончания размещения']] = banner_report_df[['Дата начала размещения','Дата окончания размещения']].astype(str)
    ...
    return banner_report_df


def multiplication_metrics(df, list_of_metrics, min_multiplier, max_multiplier):
    df[list_of_metrics] = df[list_of_metrics].astype(float)
    random_factors = np.random.uniform(min_multiplier, max_multiplier, size=(len(df), len(list_of_metrics)))
    df[list_of_metrics] = (df[list_of_metrics] + 1) * random_factors
    df[list_of_metrics] = df[list_of_metrics].round(0)
    df[list_of_metrics] = df[list_of_metrics].astype(str)
    return df