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
from custom_reports.modules.class_report import CustomReport
from my_selenium.config.default_configuration import *


class UrlTree(CustomReport):
    """ 
    Class for collecting and storing URLs for categories, products, etc.


    """

    def __init__(
        self, report_name: str = 'test', project_name: str = 'ED', report_type: str = "default"
    ):
        super().__init__(report_name, project_name, report_type)
        #
        self.at_report_df = pd.DataFrame()
        self.__set_site_url()
        self.at_default_sitemap_df = self.__create_dafault_df()
        self.at_total_rows: int = None



    def __set_site_url(self):
        if self.at_project_name == 'ED':
            self.at_site_url = ED_SITE_URL
            self.at_category_sitemap = ED_CATEGORY_SITEMAP
            self.at_tags_sitemap = ED_TAGS_SITEMAP
            self.at_other_sitemap = ED_OTHER_SITEMAP
        elif self.at_project_name == 'EM':
            self.at_site_url = EM_SITE_URL
            self.at_category_sitemap = EM_CATEGORY_SITEMAP
            self.at_tags_sitemap = EM_TAGS_SITEMAP
            self.at_other_sitemap = EM_OTHER_SITEMAP
        elif self.at_project_name == 'JB':
            self.at_site_url = JB_SITE_URL
            self.at_category_sitemap = JB_TAGS_SITEMAP
            self.at_other_sitemap = JB_OTHER_SITEMAP
        else:
            raise "Invalid project name"

    def __create_dafault_df(self):
        DEFAULT_ROWS = [[f'{self.at_project_name}','Home', f'{self.at_site_url}/'],
                        [f'{self.at_project_name}','Catalog', f'{self.at_site_url}/categories']]
        df = pd.DataFrame(DEFAULT_ROWS, columns=COLUMN)
        return df

    def get_df_from_sitemap(self, page_type, sitemap):
        '''
        Returns a DF with the URl from Sitemap.xml

        '''
        url = sitemap
        session = requests.Session()
        session.headers = HEADER
        response = session.get(url)
        if response.status_code == 200:
            xml_content = response.content
            root = ET.fromstring(xml_content)
            rows = []
            for element in root:
                rows.append(
                    [self.at_project_name, page_type, element[0].text])
            df = pd.DataFrame(rows, columns=COLUMN)
            return df
        else:
            raise("Response code is not 200")

    def selen_get_urls_from_sitemap(self):
        '''
        Test method
        
        '''
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
    
    @CustomReport.try_ping_google
    def get_full_df_with_urls(self):
        '''
        The method allows you to create a DF with all URLs from the project (ED|EM) sitemap.xml
        
        '''
        category = self.get_df_from_sitemap('Category', self.at_site_url+self.at_category_sitemap)
        category[LAST_PART_COLOMN] = category[URL_COLOMN].str.extract(r'(\d+)').fillna('')
        tags = self.get_df_from_sitemap('Tags', self.at_site_url+self.at_tags_sitemap)
        other = self.get_df_from_sitemap('Other', self.at_site_url+self.at_other_sitemap)
        tamp_df = pd.concat([self.at_default_sitemap_df, tags, other], ignore_index=True)
        tamp_df[LAST_PART_COLOMN] = ''
        site_map_df = pd.concat([tamp_df, category], ignore_index=True)
        site_map_df[PATH_COLOMN] = site_map_df[URL_COLOMN].str.replace('.*\.by', '', regex=True)
        site_map_df[URL_REDIR_COLOMN] = ''
        site_map_df[STATUS_COLOMN] = ''
        self.at_report_df = site_map_df
        return site_map_df
            

if __name__ == '__main__':
    test = UrlTree(project_name='ED')
    site_map_df = test.get_full_df_with_urls()
    print(site_map_df)