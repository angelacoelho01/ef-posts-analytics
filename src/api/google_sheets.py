from google.oauth2 import service_account
from googleapiclient.discovery import build
from utils import *
import pandas as pd
from datetime import date

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
service_sheets= build('sheets', 'v4', credentials=credentials)
print(service_sheets)


GOOGLE_SHEETS_ID = '1KZs2dfexNPll47lPk-leztbwbDpPNicEVvNpNkzoaX0'

#print(add_sheets(service_sheets, GOOGLE_SHEETS_ID, 'TEST'))
print(add_conditional_formatting_rules(service_sheets, GOOGLE_SHEETS_ID))

worksheet_name = 'TEST!'

cell_range_insert = 'A1:Z900'

value_range_body = {
     'majorDimension': 'ROWS',
     'values': values
}

service_sheets.spreadsheets().values().update(
    spreadsheetId=GOOGLE_SHEETS_ID,
    valueInputOption='USER_ENTERED',
    range=worksheet_name + cell_range_insert,
    body=value_range_body
).execute()