import numpy as np
import pandas as pd
from typing import List
import datetime
import functools
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import xml.etree.ElementTree as ET
from custom_reports.modules.class_report import CustomReport, try_ping_google
from custom_reports.config.default_configuration import *


class UrlTree(CustomReport):
    """ 
    Class for collecting and storing URLs for categories, products, etc.

    """

    def __init__(
        self, report_name: str = 'test', project_name: str = 'ED', report_type: str = "default"
    ):
        CustomReport.__init__(self, report_name, project_name, report_type)
        #
        self.at_report_df = pd.DataFrame()
        self.set_site_url()
        self.at_total_rows: int = None

    def set_site_url(self):
        if self.at_project_name == 'ED':
            self.at_site_url = ED_SITE_URL
            self.at_category_sitemap = ED_CATEGORY_SITEMAP
        elif self.at_project_name == 'EM':
            self.at_site_url = EM_SITE_URL
            self.at_category_sitemap = EM_CATEGORY_SITEMAP
        elif self.at_project_name == 'JB':
            self.at_site_url = JB_SITE_URL
            self.at_category_sitemap = JB_CATEGORY_SITEMAP
        else:
            raise "Invalid project name"
        return self.at_site_url, self.at_category_sitemap

    def create_primary_df(self):
        if self.at_project_name == 'ED':
            ...
        ...
        return self

    def get_urls_from_sitemap(self):
        url = self.at_site_url + self.at_category_sitemap
        header = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'no-cache',
            'dnt': '1',
            'pragma': 'no-cache',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
        session = requests.Session()
        session.headers = header
        # response = requests.get(url, headers = header)
        response = session.get(url)
        print(response.status_code)
        if response.status_code == 200:
            xml_content = response.content
            root = ET.fromstring(xml_content)
            # print(root)

            # Теперь вы можете работать с объектом 'root', который представляет собой корневой элемент XML.
            # Пример чтения элементов:
            headers = ['Site', 'Page_type', 'URL']
            rows = []
            for element in root:
                rows.append(
                    [self.at_project_name, 'Category', element[0].text])
                print(element[0].text)
            df = pd.DataFrame(rows, columns=headers)
            print(df)
            return df
        ...
        return

    def selen_get_urls_from_sitemap(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        driver = webdriver.Chrome(options=chrome_options)
        url = self.at_site_url + self.at_category_sitemap
        driver.get(url)
        xml_content = driver.page_source
        # root = ET.fromstring(xml_content)
        # # print(root)

        # # Теперь вы можете работать с объектом 'root', который представляет собой корневой элемент XML.
        # # Пример чтения элементов:
        # headers = ['Site', 'Page_type', 'URL']
        # rows = []
        # for element in root:
        #     rows.append(['EM', 'Category', element[0].text])
        #     print(element[0].text)
        # df = pd.DataFrame(rows, columns=headers)
        # print(df)
        return xml_content


if __name__ == '__main__':
    test = UrlTree(project_name='ED')
    xml = test.get_urls_from_sitemap()
    print(xml)