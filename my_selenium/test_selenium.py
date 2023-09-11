# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options


# chrome_options = Options()
# chrome_options.add_argument("--disable-extensions")
# driver = webdriver.Chrome(options=chrome_options)


# driver.implicitly_wait(10)
# driver.get("https://emall.by/product/1841913")
# test =  driver.execute_script("return dataLayer;")

import pandas as pd
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import xml.etree.ElementTree as ET

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://emall.by/product/1841913")

# Используем явное ожидание перед выполнением скрипта
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
# test = driver.execute_script("return dataLayer;")
# print(test)

wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
driver.get("https://edostavka.by/sitemap/categories.xml")
# test = driver.execute_script("return dataLayer;")
# print(test)

import requests

url = "https://edostavka.by/sitemap/categories.xml"
response = requests.get(url)

if response.status_code == 200:
    xml_content = response.content
    
    root = ET.fromstring(xml_content)
    # print(root)
    
    # Теперь вы можете работать с объектом 'root', который представляет собой корневой элемент XML.
    # Пример чтения элементов:
    headers = ['Site', 'Page_type', 'URL']
    rows = []
    for element in root:
        rows.append(['EM', 'Category', element[0].text])
        print(element[0].text)
    df = pd.DataFrame(rows, columns=headers)
    print(df)
else:
    print("Failed to retrieve the XML data.")
# https://edostavka.by/sitemap/6QUxaY.xml