import pandas as pd
import concurrent.futures
import requests

data = {'Column1': [i for i in range(1000)]}
df = pd.DataFrame(data)

def my_function(parameter):
    # Ваш код функции
    result = str(parameter * 2)
    return f'ttt{result}ttt'

# Создание пула потоков с 5 потоками
with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    # Задачи отправляются на выполнение в пул потоков
    # map() ожидает результаты итерации через пул потоков
    # results = executor.map(my_function, [row['Column1'] for _, row in df.iterrows()])
    results = executor.submit(my_function, [row['Column1'] for _, row in df.iterrows()])
    # print(results.result())
# Результаты доступны после завершения всех задач
# for result in results:
#     print(result)


import concurrent.futures
import urllib.request

URLS = ['http://www.foxnews.com/',
        'http://www.cnn.com/',
        'http://europe.wsj.com/',
        'http://www.bbc.co.uk/',
        'http://nonexistant-subdomain.python.org/']

# Retrieve a single page and report the URL and contents
def load_url(url, timeout):
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        return conn.read()

# We can use a with statement to ensure threads are cleaned up promptly
with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
    # Start the load operations and mark each future with its URL
    future_to_url = {executor.submit(load_url, url, 60): url for url in URLS}
    print(future_to_url)
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        
        try:
            data = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))
        else:
            print('%r page is %d bytes' % (url, len(data)))