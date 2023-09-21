import pandas as pd


from google.oauth2 import service_account
from googleapiclient.discovery import build, Resource
from google_apis.cred.credentials import GOOGLE_CREDENTIALS_JSON_PATH

API_SERVICE_NAME = "webmasters"
API_VERSION = "v3"
SCOPE = ["https://www.googleapis.com/auth/webmasters.readonly"]



def auth_using_key_file(key_filepath: str) -> Resource:
    """Authenticate using a service account key file saved locally"""

    credentials = service_account.Credentials.from_service_account_file(
        key_filepath, scopes=SCOPE
    )
    service = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

    return service

# filepath location of your service account key json file
KEY_FILE = "./service-account-key.json"

# authenticate session
service = auth_using_key_file(key_filepath=GOOGLE_CREDENTIALS_JSON_PATH)

# verify your service account has permissions to your domain
test = service.sites().list().execute()

{'siteEntry': [{'siteUrl': 'sc-domain:engineeringfordatascience.com',
   'permissionLevel': 'siteRestrictedUser'}]}
print(test)







# import searchconsole
# import pandas as pd
# import os
 
# # add folder where you downloaded your credentials
# creds = 'C:/Users/User/Desktop/Google_Indexing_API_github-master/json_json/client_secret_509265828765-1frs5jn33iia71q8hlt6gtq8dq3s8mmf.apps.googleusercontent.com.json'
 
# def authenticate(config='client_secrets.json', token='credentials.json'):
#     """Authenticate GSC"""
#     if os.path.isfile(token):
#         account = searchconsole.authenticate(client_config=config,
#                                             credentials=token)
#     else:
#         account = searchconsole.authenticate(client_config=config,
#                                         serialize=token)
#     return account
 
# account = authenticate(config=creds)
# site = 'https://emall.by/'
# months = -2
# webproperty = account[site]
# report = webproperty.query.range('today', months=months).dimension('page', 'query').get()
# df = report.to_dataframe()
# print(df)