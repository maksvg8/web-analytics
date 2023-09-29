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
from my_selenium.config.default_configuration import *
from my_selenium.modules.url_tree import *


class GetDataFromAPI(UrlTree):
    """ 
    Class for collecting and storing data for categories, products, etc. from ED_EM API


    """

    def __init__(
        self, report_name: str = 'default', project_name: str = 'ED', report_type: str = "default"
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
            return ""
        

    # def set_h1_to_default_df(self):
    #     self.at_default_sitemap_df.loc[self.at_default_sitemap_df[self.at_default_sitemap_df[PAGE_TYPE_COLOMN =]], H1_COLOMN] = 7

    #     return


    def get_json_data_from_api(self, row):
        url = f"{self.at_site_url}/_next/data/{self.at_token}{row[PATH_COLOMN]}.json?id={row[LAST_PART_COLOMN]}"
        session = requests.Session()
        session.headers = HEADER
        response = session.get(url)
        if response.status_code == 200:
            try:
                json_data = response.json()
                h1 = self.extract_h1_from_json(json_data)
                return json_data, '200', h1, row[URL_COLOMN] 
            except ValueError:
                if response.url != row[URL_COLOMN]:
                    print('Redirect')
                    return '', 'Redirect', '', response.url
                return '', 'error Invalid JSON response', '', response.url
        else:
            error_info = {
                "status_code": response.status_code
            }
            print(f"error {error_info}")
            return '', f'error Invalid status cod {response.status_code}', '', response.url


    def get_async_data(self, site_map_df):
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            future_to_row = {executor.submit(self.get_json_data_from_api, row): row for _, row in site_map_df.iterrows()}
            for future in concurrent.futures.as_completed(future_to_row):
                row = future_to_row[future]
                try:
                    json_response, status, h1, redir_url = future.result()
                    site_map_df.at[row.name, H1_COLOMN] = h1
                    site_map_df.at[row.name, STATUS_COLOMN] = status
                    site_map_df.at[row.name, URL_REDIR_COLOMN] = redir_url
                except Exception as e:
                    print(f"An error occurred for row {row.name}: {e}")
            return site_map_df
        

if __name__ == '__main__':
    project_name_list = ['ED', 'EM']
    for project in project_name_list:
        test = GetDataFromAPI(project_name=project)
        urls = test.get_full_df_with_urls()
        test.get_token()
        site_map_df = test.get_async_data(urls)
        site_map_df.loc[0:1, H1_COLOMN] = ['Главная', 'Каталог']
        print(site_map_df)
