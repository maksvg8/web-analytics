import pandas as pd

from google.oauth2 import service_account
from googleapiclient.discovery import build, Resource

from google_apis.cred.credentials import GOOGLE_CREDENTIALS_JSON_PATH


# def __get_service_google_sheets():
#     '''
#     Создание учетной записи
#     TODO: 
#     1) Добавить проверку на наличие токена
#     2) Переписать в методы класса
#     '''
#     creds_json = GOOGLE_CREDENTIALS_JSON_PATH
#     # os.path.dirname(__file__) + "/creds/sacc1.json"
#     scopes = 'https://www.googleapis.com/auth/spreadsheets'

#     creds_service = ServiceAccountCredentials.from_json_keyfile_name(
#         creds_json, scopes).authorize(httplib2.Http())
#     return build('sheets', 'v4', http=creds_service)

from google.oauth2 import service_account
from googleapiclient.discovery import build, Resource

def __get_service_google_sheets() -> Resource:
    '''
    Authenticate using a service account key file saved locally
    TODO: 
    1) Переписать в методы класса

    '''
    creds_json = GOOGLE_CREDENTIALS_JSON_PATH
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    credentials = service_account.Credentials.from_service_account_file(
        creds_json, scopes=scopes
    )
    service = build('sheets', 'v4', credentials=credentials)
    return service


def extract_rows_from_gooogle_sheets(sheet_id, sheet_range) -> pd.DataFrame:
    """
    Может читать данные из таблицы
    Для подключения к таблице необходимо выдать доступ на почту сервисного аккаунта с правами редактора
    Service Account - ga4-ed-data-api@edostavka.iam.gserviceaccount.com
    sheet_id - xxx
    https://docs.google.com/spreadsheets/d/xxx/edit#gid=0
    sheetRange - указываем с какого листа и какой размер таблицы выгружаем, пример: "'Для рассчетов'!A1:J"
    
    """
    sheet = __get_service_google_sheets().spreadsheets()
    
    # https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/get
    try:
        resp = sheet.values().get(spreadsheetId=sheet_id,
                                range=sheet_range).execute()
    except Exception as e:
        raise ConnectionError("Проблема с подключением")
    try:
        headers = resp['values'][0]
        rows = resp['values'][1:]
        df = pd.DataFrame(rows, columns=headers)
        df = df.replace('', None)
        return df
    except:
        return pd.DataFrame()

    
def add_df_to_gooogle_sheets(sheet_id, sheet_range, df):
    service = __get_service_google_sheets()
    values = [df.columns.tolist()] + df.values.tolist()
    body = {'values': values}
    request = service.spreadsheets().values().update(spreadsheetId=sheet_id, range=sheet_range, valueInputOption ='RAW', body = body)
    response = request.execute()
    ...
    return response


def clear_old_gooogle_sheet(sheet_id, sheet_range):
    batch_clear_values_request_body = {'ranges': [sheet_range]}
    service = __get_service_google_sheets()
    request = service.spreadsheets().values().batchClear(spreadsheetId=sheet_id, body=batch_clear_values_request_body)
    response = request.execute()
    ...
    return response

