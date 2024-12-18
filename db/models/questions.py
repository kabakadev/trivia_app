
from db_connection import get_db_connection
class Question:
    def __init__(self,question_text,created_by):
        self._question_id = None
        self.question_text = question_text
        self.created_by = created_by
    @property
    def question_text(self):
        return self._question_text
    @question_text.setter
    def question_text(self,question_text):
        if not isinstance(question_text, str):
            raise ValueError("the question should be a string")
        self._question_text = question_text
    @property
    def created_by(self):
        return self._created_by
    @created_by.setter
    def created_by(self, created_by):
        if not isinstance(created_by, int):
            raise ValueError("this should be passed as an int")
        self._created_by = created_by
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