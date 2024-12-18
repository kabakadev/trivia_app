
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
                CREATE TABLE IF NOT EXISTS questions(
                question_id INTEGER PRIMARY KEY,
                question_text TEXT NOT NULL,
                FOREIGN KEY (created_by) REFERENCES users(user_id)
                )
            """
            CONN.execute(sql)
    def save(self):
        with get_db_connection() as CONN:
            CURSOR = CONN.cursor()
            if self._question_id is None:
                sql = """
                    INSERT INTO questions (question_text, created_by) VALUES (?, ?)
                """
                CURSOR.execute(sql, (self.question_text, int(self.created_by)))
                self._question_id = CURSOR.lastrowid
            else:
                sql = """
                    UPDATE questions SET question_text = ?, created_by = ? WHERE question_id = ?
                """
                CURSOR.execute(sql, (self.question_text, self.created_by, self._question_id))

