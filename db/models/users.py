# from database.setup import create_tables
# from database.connection import get_db_connection
# from models.article import Article
# from models.author import Author
# from models.magazine import Magazine

from db.db_connection import get_db_connection
class User:
    def __init__(self,username,is_admin):
        self.username = username
        self.is_admin = is_admin
    @property
    def username(self):
        return self._username
    @username.setter
    def username(self,username):
        if isinstance(username,str):
            self._username = username
    @property
    def is_admin(self):
        return self._is_admin
    @is_admin.setter
    def is_admin(self,is_admin):
        self._is_admin = is_admin