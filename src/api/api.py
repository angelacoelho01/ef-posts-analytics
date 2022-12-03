from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
from datetime import date
from utils import *
from requests.conditional_formatting_between import *

current_date = date.today()

df = pd.read_csv(r'out\{}\{}\{}.csv'.format(current_date.year, current_date.month, current_date.day), delimiter=';', encoding=ENCODING)
df.sort_values(by='Data', ascending=False, inplace=True)

values = []

# Add header to values
values.append(list(df.columns.values))

df.reset_index()
for index, row in df.iterrows():
    values.append(list(row))

SERVICE_ACCOUNT_FILE = r'service_account.json'

# Load the file and authenticate the account
credentials = service_account.Credentials.from_service_account_file(
    filename=SERVICE_ACCOUNT_FILE
)

# Construct the google service instance
service= build('sheets', 'v4', credentials=credentials)
print(service)


SPREADSHEET_ID = '1KZs2dfexNPll47lPk-leztbwbDpPNicEVvNpNkzoaX0'

red = Between(2021327580, 3, 4, 0, 999, 0, 200, '#ea9999')
print(red.send_request(service, SPREADSHEET_ID))

worksheet_name = 'TEST!'

cell_range_insert = 'A1:Z900'

value_range_body = {
     'majorDimension': 'ROWS',
     'values': values
}

service.spreadsheets().values().update(
    spreadsheetId=SPREADSHEET_ID,
    valueInputOption='USER_ENTERED',
    range=worksheet_name + cell_range_insert,
    body=value_range_body
).execute()