# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options


# chrome_options = Options()
# chrome_options.add_argument("--disable-extensions")
# driver = webdriver.Chrome(options=chrome_options)


# driver.implicitly_wait(10)
# driver.get("https://emall.by/product/1841913")
# test =  driver.execute_script("return dataLayer;")


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://emall.by/product/1841913")

# Используем явное ожидание перед выполнением скрипта
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
test = driver.execute_script("return dataLayer;")
print(test)

wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
driver.get("https://emall.by/product/533337")
test = driver.execute_script("return dataLayer;")
print(test)

import requests

url = "https://emall.by/sitemap/categories.xml"
response = requests.get(url)

if response.status_code == 200:
    sitemap_content = response.text
    print(sitemap_content)
else:
    print("Failed to retrieve the sitemap.")