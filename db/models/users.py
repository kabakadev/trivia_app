# from database.setup import create_tables
# from database.connection import get_db_connection
# from models.article import Article
# from models.author import Author
# from models.magazine import Magazine

from db_connection import get_db_connection
class User:
    def __init__(self,username,is_admin):
        self._user_id = None
        self.username = username
        self.is_admin = is_admin
    @property
    def username(self):
        return self._username
    @username.setter
    def username(self,username):
        if isinstance(username,str):
            self._username = username
        else:
            raise ValueError("username must be a string")
    @property
    def is_admin(self):
        return self._is_admin
    @is_admin.setter
    def is_admin(self, is_admin):
        if isinstance(is_admin, bool):
            self._is_admin = is_admin
        else:
            raise ValueError("is_admin must be a boolean")
    @classmethod
    def create_table(cls):
        CONN = get_db_connection()
        CURSOR = CONN.cursor()
        sql = """
            CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            is_admin BOOLEAN DEFAULT FALSE
            )
            """
        CURSOR.execute(sql)
        CONN.commit()
        CONN.close()
    def save(self):
        CONN = get_db_connection()
        CURSOR = CONN.cursor()
        sql_check = "SELECT * FROM users WHERE username = ?"
        existing_user = CURSOR.execute(sql_check,(self.username,)).fetchone()
        if existing_user:
            raise ValueError(f"username '{self.username}' already exists")
        if self._user_id is None:  
                sql = """
                INSERT INTO users (username, is_admin) VALUES (?, ?)
                """
                CURSOR.execute(sql, (self.username, int(self.is_admin)))
                self._user_id = CURSOR.lastrowid 
        else:  
            sql = """
                UPDATE users SET username = ?, is_admin = ? WHERE user_id = ?
                """
            CURSOR.execute(sql, (self.username, self.is_admin, self._user_id))
        CONN.commit()
        CONN.close()
    @classmethod
    def get_user_by_id(cls,user_id):
        CONN = get_db_connection()
        CURSOR = CONN.cursor()
        sql = """
            SELECT *
            FROM users

            WHERE user_id = ?
            """
        row = CURSOR.execute(sql,(user_id,)).fetchone()
        if row:
            user = cls(row[1], bool(row[2])) 
            user._user_id = row[0] 
            return user
        return None 



user1 = User("justin",True)
user2 = User("Ian" ,False)
user1.create_table()
user2.create_table()
user1.save()
user2.save()
user = user1.get_user_by_id(1)
user_get = user2.get_user_by_id(2)

if user:
    print(f"User found: {user.username}")
else:
    print("User not found.")
if user_get:
    print(f"User found: {user_get.username}")
else:
    print("User not found.")

