import requests
import datetime
import pandas as pd

DIM_CAMPAIGN_REPORT = "ym:s:date,ym:s:<attribution>UTMCampaign"
METR_CAMPAIGN_REPORT = "ym:s:visits,ym:s:users,ym:s:ecommercePurchases,ym:s:ecommerce<currency>ConvertedRevenue"

YM_ED_COUNTER_ID = "89127076"
FILTER_ED_CAMPAIGN = "ym:s:<attribution>UTMCampaign=~'.*_ed_.*' AND NOT(ym:s:<attribution>UTMCampaign=~'.*(blogg|smm_|emall|edostavka).*')"


YM_TOKEN = "y0_AgAAAABaPiH5AAoGKAAAAADk-0IaNKLrObttQOOgBjtexDD_-vF8Nys"

at_start_date = "2023-10-1"
at_end_date = "2023-10-18"

dt_today = datetime.date.today()
dt_yesterday = str(dt_today - datetime.timedelta(days=20))




def request_ym_data():
        # параметры запроса
        params = {
            "dimensions": DIM_CAMPAIGN_REPORT,
            "metrics": METR_CAMPAIGN_REPORT,
            "ids": YM_ED_COUNTER_ID,
            "date1": at_start_date,
            "date2": at_end_date,
            # ym:s:deviceCategory!='mobile'
            "filters": FILTER_ED_CAMPAIGN,
            "accuracy": 1,
            "limit": 100000,
            "offset": 1,
            "pretty": False,
        }

        # Формируем URL для выполнения запроса
        try:
            url = "https://api-metrika.yandex.net/stat/v1/data?"

            # Отправляем запрос к API
            headers = {"Authorization": f"OAuth {YM_TOKEN}"}
            response = requests.get(url, headers=headers, params=params)
            # Обрабатываем результаты
            if response.status_code != 200:
                print(
                    "Произошла ошибка при выполнении запроса:",
                    f"{response.status_code}",
                    f"{response.text}",
                )
                exit()
            else:
                data = response
                return data
                at_total_rows = data["total_rows"]
                at_ym_data = data
                if self.at_total_rows == 0:
                    print("Произошла ошибка при выполнении запроса: Пустое тело ответа")
                    exit()
                return data, self.at_total_rows
        except Exception as e:
            raise e
        


if __name__=="__main__":
    
    a = request_ym_data()
    # df = pd.read_json(a)
    print(a.json())
