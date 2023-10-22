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


class DataFromEDAPI(UrlTree):
    ''' 
    Class for collecting and storing data for categories, products, etc. from ED_EM API


    '''

    def __init__(
        self, report_name: str = 'default', project_name: str = 'ED', report_type: str = 'default'
    ):
        super().__init__(report_name, project_name, report_type)
        #
        self.at_report_df = pd.DataFrame()
        self.at_total_rows: int = None



    def get_token(self):
        '''
        Obtain the token needed to extract data from the site's json response
        
        '''
        url = self.at_site_url+'/'
        response = requests.get(url, headers=HEADER)
        if response.status_code == 200:
            html_content = response.text
            # Ищем значение в src атрибуте <script> тега
            match = re.search(r'<script src="/_next/static/([^/]+)/_buildManifest.js" defer="">', html_content)
            if match:
                self.at_token = match.group(1)
                print('Найденное значение:', self.at_token)
            else:
                raise('Значение не найдено')
        else:
            raise('Ошибка при получении страницы')


    def extract_h1_from_json(self, response):
        try:
            h1_value = response.get('pageProps', {}).get('page', {}).get('seo', {}).get('h1', '')
            return h1_value
        except:
            return ''


    def get_json_data_from_api(self, row):
        '''
        This method allows you to get data from the json response json of the site, such as h1 and the status of the response
        
        '''
        url = f'{self.at_site_url}/_next/data/{self.at_token}{row[PATH_COLOMN]}.json?id={row[LAST_PART_COLOMN]}'
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
                'status_code': response.status_code
            }
            print(f'error {error_info}')
            return '', f'error Invalid status cod {response.status_code}', '', response.url


    def get_tread_data(self, site_map_df):
        '''
        Allows you to retrieve page data in multiple threads
        
        '''
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
                    print(f'An error occurred for row {row.name}: {e}')
            return site_map_df
        

if __name__ == '__main__':
    project_name_list = ['ED', 'EM']
    for project in project_name_list:
        test = DataFromEDAPI(project_name=project)
        urls = test.get_full_df_with_urls()
        test.get_token()
        site_map_df = test.get_tread_data(urls)
        site_map_df.loc[0:1, H1_COLOMN] = ['Главная', 'Каталог']
        mask = site_map_df[URL_REDIR_COLOMN].str.contains(test.at_site_url)

        filtered_df = site_map_df[mask]
        print(filtered_df)
