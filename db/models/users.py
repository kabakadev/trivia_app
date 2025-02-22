from db import get_db_connection
class User:
    all = {}
    def __init__(self,username,is_admin):
        self._user_id = None
        self.username = username
        self.is_admin = is_admin
    @property
    def user_id(self):
        return self._user_id
    @property
    def username(self):
        return self._username
    @username.setter
    def username(self,username):
        if not isinstance(username,str):
            raise ValueError("username must be a string") 
        self._username = username
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
        with get_db_connection() as CONN:
            sql = """
                CREATE TABLE IF NOT EXISTS users(
                user_id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                is_admin BOOLEAN DEFAULT FALSE
                )
            """
            CONN.execute(sql)
    def save(self):
        with get_db_connection() as CONN:
            CURSOR = CONN.cursor()
            sql_check = "SELECT * FROM users WHERE username = ?"
            existing_user = CURSOR.execute(sql_check,(self.username,)).fetchone()
            if existing_user:
                raise ValueError(f"username '{self.username}' exists already.")
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
    @classmethod
    def instance_from_db(cls,row):
        user = cls.all.get(row[0])
        if user:
            user.username = row[1]
            user.is_admin = bool(row[2])
        else:
            user = cls(row[1], bool(row[2]))
            user._user_id = row[0]
            cls.all[user._user_id] = user
        return user

    @classmethod
    def get_all_users(cls):
        with get_db_connection() as CONN:
            CURSOR = CONN.cursor()
            sql = "SELECT * FROM users"
            rows = CURSOR.execute(sql).fetchall()
            return [cls.instance_from_db(row) for row in rows]
    @classmethod
    def get_user_by_id(cls,user_id):
        with get_db_connection() as CONN:
      
            CURSOR = CONN.cursor()
            sql = """
                SELECT *
                FROM users

                WHERE user_id = ?
                """
            row = CURSOR.execute(sql,(user_id,)).fetchone()
            return cls.instance_from_db(row) if row else None
    @classmethod
    def get_user_by_username(cls,username):
        with get_db_connection() as CONN:
            CURSOR = CONN.cursor()
            sql = """
                SELECT *
                FROM users

                where username = ?
                    """ 
            row = CURSOR.execute(sql,(username,)).fetchone()
            return cls.instance_from_db(row) if row else None
    def delete(self):
        if self._user_id == None:
            raise ValueError("this user currently does not exist in the database")
        with get_db_connection() as CONN:
            CURSOR = CONN.cursor()

            sql = """DELETE FROM users WHERE user_id = ?  """
            CURSOR.execute(sql,(self._user_id,))
            self._user_id = None
    @classmethod
    def drop_table(cls):
       with get_db_connection() as CONN:
            CURSOR = CONN.cursor()

            sql = """DROP TABLE IF EXISTS users"""
            CURSOR.execute(sql)
        



