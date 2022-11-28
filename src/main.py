from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests

URL = "https://www.easyfuture.pt/artigos"
DATA_ID_HEADER = 'pgi'

posts = []

page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

class Post:
    def __init__(self, id, data_id):
        self.postID = id
        self.data_id = data_id
        self.title = ''
        self.author = ''
        self.views = 0
        self.likes = 0

    def get_id(self):
        return self.postID
    
    def get_data_id(self):
        return self.data_id
    
    def get_title(self):
        return self.title
    
    def get_author(self):
        return self.author
    
    def get_views(self):
        return self.views
    
    def get_likes(self):
        return self.likes
    
    def set_title(self, title):
        self.title = title

    def set_views(self, views):
        self.views = views

    def set_likes(self, likes):
        self.likes = likes

    def set_author(self, author):
        self.author = author

    def __str__(self) -> str:
        return '[{}]\nTitle: {}\nAuthor: {}\nViews: {}\nLikes: {}'.format(
                self.data_id, 
                self.title,
                self.author,
                self.views,
                self.likes
                )

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
        post_author = data.find_all('span', {'data-hook': 'user-name'})[0].text.rstrip()
        post_views = data.find_all('span', {'class': 'eYQJQu'})[0].text
        post_likes = data.find_all('span', {'class': 'FYRNvd like-button-with-count__like-count'})[0].text

        post.set_title(post_title)
        post.set_author(post_author)
        post.set_views(int(post_views))
        post.set_likes(int(post_likes))
        print(post)