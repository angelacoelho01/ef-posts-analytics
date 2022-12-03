from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
from datetime import date
from utils import *
from sheets.sheet import Sheet

# Set up google sheets
SERVICE_ACCOUNT_FILE = r'service_account.json'
SPREADSHEET_ID = '1KZs2dfexNPll47lPk-leztbwbDpPNicEVvNpNkzoaX0'

# Load the file and authenticate the account
credentials = service_account.Credentials.from_service_account_file(
    filename=SERVICE_ACCOUNT_FILE
)

# Construct the google service instance
service= build('sheets', 'v4', credentials=credentials)

# Load data to export
current_date = date.today()

df = pd.read_csv(r'out\{}\{}\{}.csv'.format(current_date.year, current_date.month, current_date.day), delimiter=';', encoding=ENCODING)
df.sort_values(by='Data', ascending=False, inplace=True)

# Add general sheet
# TODO: Create sheets and conditional formatting rules
general_sheet = Sheet('Geral')
general_sheet.set_values(get_values_from_dataset(df))
general_sheet.update_sheet(service, SPREADSHEET_ID)


# Add sheet by author
authors = sorted(df['Autor'].unique())

for author in authors:
    df_author = df.copy()
    df_author = df_author[df_author['Autor'] == author]
    author_sheet = Sheet(author)
    df_author.drop('Autor', inplace=True, axis=1)
    author_sheet.set_values(get_values_from_dataset(df_author))
    author_sheet.update_sheet(service, SPREADSHEET_ID)


# Add sheet by category
df_category = df.copy()

# Get number of articles related to a certain category
df_count = df_category.groupby('Categoria', as_index=False).count()
df_count['Número de Artigos'] = df_count['Título']
df_count = df_count[['Categoria', 'Número de Artigos']]

# Get total number of views of a certain article
df_sum = df_category.groupby('Categoria', as_index=False).sum()
df_sum['Número Total de Visualizações'] = df_sum['Visualizações']
df_sum = df_sum[['Categoria', 'Número Total de Visualizações']]

# Get mean visualizations per article
df_mean = df_category.groupby('Categoria', as_index=False).mean().round(0)
df_mean['Média de Visualizações'] = df_mean['Visualizações']
df_mean = df_mean[['Categoria', 'Média de Visualizações']]

# Merge the above 3 datasets by 'Categoria'
df_category = pd.merge(df_count, df_sum, on='Categoria')
df_category = pd.merge(df_category, df_mean, on='Categoria')

category_sheet = Sheet('Por Categoria')
category_sheet.set_values(get_values_from_dataset(df_category))
category_sheet.update_sheet(service, SPREADSHEET_ID)