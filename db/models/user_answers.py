from db_connection import get_db_connection
class UserAnswer:
    def __init__(self,user_id,question_id,choice_id):
        self._user_answer_id = None
        self.user_id = user_id
        self.question_id = question_id
        self.choice_id = choice_id
    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        if not isinstance(user_id, int):
            raise ValueError("sser id must be an integer")
        self._user_id = user_id
    @property
    def question_id(self):
        return self._question_id

    @question_id.setter
    def question_id(self, question_id):
        if not isinstance(question_id, int):
            raise ValueError("question id must be an integer")
        self._question_id = question_id
    @property
    def choice_id(self):
        return self._choice_id

    @choice_id.setter
    def choice_id(self, choice_id):
        if not isinstance(choice_id, int):
            raise ValueError("choice id must be an integer")
        self._choice_id = choice_id
    @classmethod
    def create_table(cls):
        with get_db_connection() as CONN:
            CURSOR = CONN.cursor()
            sql = """
                CREATE TABLE IF NOT EXISTS user_answers(
                user_answer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                question_id INTEGER,
                choice_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (question_id) REFERENCES questions(question_id),
                FOREIGN KEY (choice_id) REFERENCES choices(choice_id)
                )
                """
            CURSOR.execute(sql)