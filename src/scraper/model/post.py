from datetime import date

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
