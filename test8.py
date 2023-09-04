import pandas as pd
import requests

# Создаем заголовки
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
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}

# Функция для выполнения запроса и извлечения JSON


def fetch_json(project):
    if project == "ED":
        url = f"https://edostavka.by/_next/data/QEQzJX2lKmJ54x42NESov/category/5183.json?id=5183"
    elif project == "EM":
        url = f"https://emall.by/_next/data/1GzjMux1hWSC_vXtG809m/category/5183.json?id=5183"
    else:
        return None

    session = requests.Session()
    session.headers = header
    response = session.get(url)

    # Проверяем успешность запроса и наличие контента
    if response.status_code == 200 and response.content:
        try:
            json_data = response.json()
            return json_data
        except ValueError:
            return {"error": "Invalid JSON response"}
    else:
        error_info = {
            "status_code": response.status_code,
            "error_message": response.text
        }
        return {"error": error_info}


def extract_h1(response):
    try:
        h1_value = response.get("pageProps", {}).get(
            "page", {}).get("seo", {}).get("h1", "")
        return h1_value
    except Exception as e:
        return f"Error: {e}"


import re
import requests

# Создаем заголовки
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
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}

url = "https://edostavka.by"
response = requests.get(url, headers=header)

if response.status_code == 200:
    html_content = response.text

    # Ищем значение в src атрибуте <script> тега
    match = re.search(r'<script src="/_next/static/([^/]+)/_buildManifest.js" defer="">', html_content)
    
    if match:
        script_value = match.group(1)
        print("Найденное значение:", script_value)
    else:
        print("Значение не найдено")
else:
    print("Ошибка при получении страницы:", response.status_code)

# Выводим информацию о датафрейме с результатами
response = fetch_json('ED')
h1 = extract_h1(response)
print(h1)
