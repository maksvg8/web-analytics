from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(10)
driver.get("https://emall.by/product/1249068")
email_form = driver.find_element(By.ID, 'testing_form')