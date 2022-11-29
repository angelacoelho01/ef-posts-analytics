from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests
from utils import *
from datetime import date
import csv
import os

class Post:
    def __init__(self, id, data_id):
        self.postID = id
        self.data_id = data_id
        self.title = ''
        self.category = ''
        self.author = ''
        self.views = 0
        self.likes = 0
        self.publication_date = date.today()

    def get_id(self):
        return self.postID
    
    def get_data_id(self):
        return self.data_id
    
    def get_title(self):
        return self.title

    def get_category(self):
        return self.category
    
    def get_author(self):
        return self.author
    
    def get_views(self):
        return self.views
    
    def get_likes(self):
        return self.likes
    
    def get_publication_date(self):
        return self.publication_date
    
    def set_title(self, title):
        self.title = title

    def set_category(self, category):
        self.category = category

    def set_views(self, views):
        self.views = views

    def set_likes(self, likes):
        self.likes = likes

    def set_author(self, author):
        self.author = author

    def set_publication_date(self, publication_date):
        self.publication_date = publication_date

    def __str__(self) -> str:
        return '[{}]\n\tTitle: {}\n\tCategory: {}\n\tPublication Date: {}\n\tAuthor: {}\n\tViews: {}\n\tLikes: {}\n'.format(
                self.data_id, 
                self.title,
                self.category,
                self.publication_date,
                self.author,
                self.views,
                self.likes
                )

posts = []

page = requests.get(BASE_URL)
soup = BeautifulSoup(page.content, "html.parser")
num_pages = get_num_pages(soup)

for num_page in range(1, num_pages+1):
    current_page = requests.get(PAGE_URL + str(num_page))
    soup =BeautifulSoup(current_page.content, "html.parser")

    # Get all posts 'data-id'
    index = 0
    for section in soup.findAll('div', id='pro-gallery-margin-container-pro-blog'):
        for element in section:
            post_id = element.attrs.get('data-id')
            post_data_id = '{}{}_{}'.format(
                    DATA_ID_HEADER, 
                    post_id.replace('-', ''), 
                    str(index)
                    )

            posts.append(Post(post_id, post_data_id))

            index += 1

    for post in posts:
        post_data = soup.findAll('div', id=post.get_data_id())
        for data in post_data:
            post_title = data.attrs.get('aria-label').rstrip()
            post_category = data.find_all('a', {'class': 'pratMU dqpczu'})
            post_author = data.find_all('span', {'data-hook': 'user-name'})[0].text.rstrip()
            post_publication_date = data.find_all('span', {'data-hook': 'time-ago'})[0].text.rstrip()
            post_views = data.find_all('span', {'class': 'eYQJQu'})[0].text
            post_likes = data.find_all('span', {'class': 'FYRNvd like-button-with-count__like-count'})[0].text
            
            post.set_title(post_title)
            post.set_category(post_category[0].text.rstrip() if len(post_category) != 0 else 'Não especificado')
            post.set_publication_date(parse_date(post_publication_date))
            post.set_author(post_author)
            post.set_views(int(post_views.replace('.', '')))
            post.set_likes(int(post_likes.replace('.', '')))

current_date = date.today()
out_path = r'out\{}\{}'.format(current_date.year, current_date.month)
if not os.path.exists(out_path):
    os.makedirs(out_path)

out_file_path = r'{}\{}.csv'.format(out_path, current_date.day)
f = open(out_file_path, 'w', newline='')
writer = csv.writer(f, delimiter=';')

# Write header to csv file
writer.writerow(CSV_HEADER)

for post in posts:
    # Write the post data in the csv file
    writer.writerow([
        post.get_category(),
        post.get_title(),
        post.get_author(),
        post.get_views(),
        post.get_likes(),
        post.get_publication_date()
    ])



f.close()
