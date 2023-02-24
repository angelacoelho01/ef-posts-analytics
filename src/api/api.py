from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
from datetime import date
from sheets.sheet import Sheet
from statistics import mean
from utils import *
from requests.add_sheet import *
from requests.add_conditional_formatting import *
from requests.update_cells import *
import time

def add_stats_conditional_formatting(service, spreadsheet_id, sheet_id, min, q1, mean, q3, max, max_outlier, 
                                     start_col_index, end_col_index, end_row_index):
    bounds = [min-1, q1, mean, q3, max, max_outlier]

    color_index = 0
    for lower_bound, upper_bound in zip(bounds, bounds[1:]):
        add_conditional_formatting = AddConditionalFormatting(
            sheet_id=sheet_id,
            start_column_index=start_col_index,
            end_column_index=end_col_index,
            start_row_index=0,
            end_row_index=end_row_index,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            color=COLORS[color_index]
        )

        add_conditional_formatting.send_request(service, spreadsheet_id)
        
        color_index += 1
        time.sleep(1)

# Load data to export
current_date = date.today()

df = pd.read_csv(r'out\{}\{}\{}.csv'.format(current_date.year, current_date.month, current_date.day), delimiter=';', encoding=ENCODING)
df.sort_values(by='Data', ascending=False, inplace=True)

# Get all the views values
views = [value[3] for value in get_values_from_dataset(df)[1:]]
views_outliers = get_outliers(views)
views_max_outlier = max(views_outliers)
views_no_outliers = [value for value in views if value not in views_outliers]
views_max = max(views_no_outliers)
views_min = min(views_no_outliers)
views_mean = int(mean(views_no_outliers))
views_q1 = get_q1(views_min, views_mean)
views_q3 = get_q3(views_mean, views_max)

# Get all the like values
likes = [value[4] for value in get_values_from_dataset(df)[1:]]
likes_outliers = get_outliers(likes)
likes_max_outlier = max(likes_outliers)
likes_no_outliers= [value for value in likes if value not in likes_outliers]
likes_max = max(likes_no_outliers)
likes_min = min(likes_no_outliers)
likes_mean = int(mean(likes_no_outliers))
likes_q1 = get_q1(likes_min, likes_mean)
likes_q3 = get_q3(likes_mean, likes_max)

# Set up google sheets
SERVICE_ACCOUNT_FILE = r'service_account.json'
SPREADSHEET_ID = '1KZs2dfexNPll47lPk-leztbwbDpPNicEVvNpNkzoaX0'

# Load the file and authenticate the account
credentials = service_account.Credentials.from_service_account_file(
    filename=SERVICE_ACCOUNT_FILE
)


# Construct the google service instance
service= build('sheets', 'v4', credentials=credentials)

# Get all the current sheets in the spreadsheet
sheets = []
sheets_properties = service.spreadsheets().get(
        spreadsheetId=SPREADSHEET_ID
    ).execute().get('sheets')

# for sheet_property in sheets_properties:
#     sheets.append(sheet_property.get('properties').get('title'))

# # Add general sheet
# general_sheet = AddSheet('Geral')
# general_sheet.set_values(get_values_from_dataset(df))
# general_sheet.update_sheet(service, SPREADSHEET_ID, sheets)

# general_sheet_id = 0
# for sheets in sheets_properties:
#     if (sheets['properties']['title'] == 'Geral'):
#         general_sheet_id = sheets['properties']['sheetId']

# # Add sheet by author
# authors = sorted(df['Autor'].unique())
# authors_num_posts = {}
# authors_num_posts['Geral'] = len(df)

# for author in authors:
#     if author == '-':
#         continue

#     df_author = df.copy()
#     df_author = df_author[df_author['Autor'] == author]
#     df_author.drop('Autor', inplace=True, axis=1)

#     # Add total number of posts and the mean for views and likes
#     author_values = []

#     # Get the mean of views and likes
#     author_views = df_author['Visualizações'].mean().round(0)
#     author_likes = df_author['Gostos'].mean().round(0)

#     # Create a sheet for each author with the relative values
#     if author != 'Easy Future':
#         author_sheet = AddSheet(author)

#     else:
#         author_sheet = AddSheet(author)

#         df_author_ef = df.copy()
#         df_author_ef = df_author_ef[df_author_ef['Autor'] == '-']
#         df_author_ef.drop('Autor', inplace=True, axis=1)

#         author_views += df_author_ef['Visualizações']
#         author_likes += df_author_ef['Gostos']

#         df_author = pd.concat([df_author, df_author_ef])

#     author_sheet.set_values(get_values_from_dataset(df_author))
#     author_views_mean = author_views.mean().round(0)
#     author_likes_mean = author_likes.mean().round(0)

#     author_values += [
#         [],
#         [],
#         ['', 'Visualizações', 'Gostos'],
#         ['Média', author_views_mean, author_likes_mean],
#         [],
#         ['Número Total de Posts', len(df_author)]
#     ]

#     authors_num_posts[author] = len(df_author)

#     author_sheet.add_values(author_values)
#     author_sheet.update_sheet(service, SPREADSHEET_ID, sheets)

# # Get all the current sheets in the spreadsheet
# sheets_properties = service.spreadsheets().get(
#         spreadsheetId=SPREADSHEET_ID
#     ).execute().get('sheets')

# # Add conditional formatting to every sheet
# for sheet in sheets_properties:
#     title = sheet['properties']['title']

#     # Ignore 'Código de Cores' sheet
#     if title == 'Código de Cores':
#         continue

#     start_column_index = 3 if title == 'Geral' else 2
#     end_column_index = 4 if title == 'Geral' else 3

#     sheet_id = sheet['properties']['sheetId']
#     num_posts = authors_num_posts[title]

#     print(title)

#     # Conditional Formatting for Views
#     add_stats_conditional_formatting(
#         service=service,
#         spreadsheet_id=SPREADSHEET_ID,
#         sheet_id=sheet_id,
#         min=views_min,
#         q1=views_q1,
#         mean=views_mean,
#         q3=views_q3,
#         max=views_max,
#         max_outlier=views_max_outlier,
#         start_col_index=start_column_index,
#         end_col_index=end_column_index,
#         end_row_index=num_posts+1
#     )

#     # Conditional Formatting for Likes
#     add_stats_conditional_formatting(
#         service=service,
#         spreadsheet_id=SPREADSHEET_ID,
#         sheet_id=sheet_id,
#         min=likes_min,
#         q1=likes_q1,
#         mean=likes_mean,
#         q3=likes_q3,
#         max=likes_max,
#         max_outlier=likes_max_outlier,
#         start_col_index=start_column_index+1,
#         end_col_index=end_column_index+1,
#         end_row_index=num_posts+1
#     )

# exit()
print(df)

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

category_sheet = AddSheet('Por Categoria')
category_sheet.set_values(get_values_from_dataset(df_category))
category_sheet.update_sheet(service, SPREADSHEET_ID, sheets)