import numpy as np
import pandas as pd
from typing import List
import datetime
import functools
import re
import requests
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import xml.etree.ElementTree as ET
from custom_reports.modules.class_report import try_ping_google
from my_selenium.config.default_configuration import *
from my_selenium.modules.url_tree import *



# # Создаем заголовки
# header = {
#     'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
#     'accept-encoding':'gzip, deflate, br',
#     'accept-language':'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
#     'cache-control':'no-cache',
#     'dnt': '1',
#     'pragma': 'no-cache',
#     'sec-fetch-mode': 'navigate',
#     'sec-fetch-site': 'none',
#     'sec-fetch-user': '?1',
#     'upgrade-insecure-requests': '1',
#     'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
# }

# # Функция для выполнения запроса и извлечения JSON
# def fetch_json(row):
#     if row["Domain"] == "https://edostavka.by":
#         url = f"https://edostavka.by/_next/data/W8J8cwtI4GSxWu3euE2du/category/categories.json?id=categories"
#     elif row["Domain"] == "https://emall.by":
#         url = f"https://emall.by/_next/data/1GzjMux1hWSC_vXtG809m/category/{row['LastSegment']}.json?id={row['LastSegment']}"
#     else:
#         return None
    
#     session = requests.Session()
#     session.headers = header
#     response = session.get(url)
    
#     # Проверяем успешность запроса и наличие контента
#     if response.status_code == 200 and response.content:
#         try:
#             json_data = response.json()
#             return json_data
#         except ValueError:
#             return {"error": "Invalid JSON response"}
#     else:
#         error_info = {
#             "status_code": response.status_code,
#             "error_message": response.text
#         }
#         return {"error": error_info}

# # Добавляем новый столбец для хранения результатов запросов
# destination_df_copy["JSONResponse"] = ""

# # Проходим по каждой строке датафрейма и выполняем запрос
# for index, row in destination_df_copy.iterrows():
#     json_response = fetch_json(row)
#     destination_df_copy.at[index, "JSONResponse"] = json_response
    
#     # Выводим информацию о текущей строке и результате запроса
#     print(f"Processing row {index}:")

# # Выводим информацию о датафрейме с результатами
# print(destination_df_copy)



# def extract_h1(response):
#     try:
#         h1_value = response.get("pageProps", {}).get("page", {}).get("seo", {}).get("h1", "")
#         return h1_value
#     except Exception as e:
#         return f"Error: {e}"
    

# with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
#     future_to_row = {executor.submit(fetch_and_save_json, row): row for _, row in destination_df_copy.iterrows()}
    
#     for future in as_completed(future_to_row):
#         row = future_to_row[future]
#         try:
#             json_response = future.result()
#             destination_df_copy.at[row.name, "JSONResponse"] = json_response
#             print(f"Processing row {row.name}:")
#         except Exception as e:
#             print(f"An error occurred for row {row.name}: {e}")

# # Выводим информацию о датафрейме с результатами
# print(destination_df_copy)




class GetDataFromAPI(UrlTree):
    """ 
    Class for collecting and storing data for categories, products, etc. from ED_EM API


    """

    def __init__(
        self, report_name: str = 'test', project_name: str = 'ED', report_type: str = "default"
    ):
        CustomReport.__init__(self, report_name, project_name, report_type)
        UrlTree.__init__(self, report_name, project_name, report_type)
        #
        self.at_report_df = pd.DataFrame()
        self.at_total_rows: int = None


    def get_token(self):
        url = self.at_site_url+'/'
        response = requests.get(url, headers=HEADER)
        if response.status_code == 200:
            html_content = response.text
            # Ищем значение в src атрибуте <script> тега
            match = re.search(r'<script src="/_next/static/([^/]+)/_buildManifest.js" defer="">', html_content)
            if match:
                self.at_token = match.group(1)
                print("Найденное значение:", self.at_token)
            else:
                raise("Значение не найдено")
        else:
            raise("Ошибка при получении страницы")


    def extract_h1_from_json(self, response):
        try:
            h1_value = response.get("pageProps", {}).get("page", {}).get("seo", {}).get("h1", "")
            return h1_value
        except:
            return "No h1"
        
    # def 

    def get_json_data_from_api(self, row):
        url = f"{self.at_site_url}/_next/data/{self.at_token}{row[PATH_COLOMN]}.json?id={row[LAST_PART_COLOMN]}"
        session = requests.Session()
        session.headers = HEADER
        response = session.get(url)
        if response.status_code == 200:
            try:
                json_data = response.json()
                h1 = self.extract_h1_from_json(json_data)
                return json_data, h1, row[URL_COLOMN] 
            except ValueError:
                if response.url != row[URL_COLOMN]:
                    print('Redirect')
                    return '', '', response.url
                return "error Invalid JSON response"
        else:
            error_info = {
                "status_code": response.status_code
            }
            print(f"error {error_info}")



    def get_async_data(self, site_map_df):
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            future_to_row = {executor.submit(self.get_json_data_from_api, row): row for _, row in site_map_df.iterrows()}
            
            for future in concurrent.futures.as_completed(future_to_row):
                row = future_to_row[future]
                try:
                    json_response, h1, redir_url = future.result()
                    site_map_df.at[row.name, H1_COLOMN] = h1
                    site_map_df.at[row.name, URL_REDIR_COLOMN] = redir_url
                    test_h1 = self.extract_h1_from_json(json_response)
                    # print(test_h1, '+', h1)
                except Exception as e:
                    print(f"An error occurred for row {row.name}: {e}")
            return site_map_df
        
if __name__ == '__main__':
    test = GetDataFromAPI(project_name='ED')
    urls = test.get_full_df_with_urls()
    test.get_token()
    site_map_df = test.get_async_data(urls)
    print(site_map_df)
    test.overwriting_old_csv_report(site_map_df)

    test = GetDataFromAPI(project_name='EM')
    urls = test.get_full_df_with_urls()
    test.get_token()
    site_map_df = test.get_async_data(urls)
    print(site_map_df)
    test.overwriting_old_csv_report(site_map_df)

    # i=0
    # for index, row in urls.iterrows():
    #     json_response = test.get_json_data(row)
    #     h1 = test.extract_h1(json_response)
    #     # Выводим информацию о текущей строке и результате запроса
    #     print(i)
    #     print(h1)
    #     i+=1
