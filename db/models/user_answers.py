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
    
    def save(self):
        with get_db_connection() as CONN:
            CURSOR = CONN.cursor()
            if self._user_answer_id is None:
                sql = """
                INSERT INTO user_answers (user_id, question_id, choice_id) VALUES (?, ?, ?)
                """
            
                CURSOR.execute(sql, (self.user_id, self.question_id, self.choice_id))
                self._user_answer_id = CURSOR.lastrowid
            else:
                sql = """
                UPDATE user_answers SET user_id = ?, question_id = ?, choice_id = ?, WHERE user_answer_id = ?
                """
         
                CURSOR.execute(sql, (self.user_id, self.question_id, self.choice_id, self._user_answer_id))
    @classmethod
    def get_user_answers_by_user_id(cls, user_id):
        with get_db_connection() as CONN:
            CURSOR = CONN.cursor()
            sql = """
                SELECT *
                FROM user_answers
                WHERE user_id = ?
                """
            CURSOR.execute(sql, (user_id,))
            rows = CURSOR.fetchall()
            user_answers = []
            if rows:
                for row in rows:
                    user_answer = cls(row[1], row[2], row[3])
                    user_answer._user_answer_id = row[0]
                    user_answers.append(user_answer)
                return user_answers
            return None
    @classmethod
    def get_user_answers_by_question_id(cls, question_id):
        with get_db_connection() as CONN:
            CURSOR = CONN.cursor()
            sql = """
                SELECT *
                FROM user_answers
                WHERE question_id = ?
                """
            CURSOR.execute(sql, (question_id,))
            rows = CURSOR.fetchall()
            user_answers = []
            if rows:
                for row in rows:
                    user_answer = cls(row[1], row[2], row[3])
                    user_answer._user_answer_id = row[0]
                    user_answers.append(user_answer)
                return user_answers
            return None
    @classmethod
    def get_user_answer_by_user_and_question_id(cls, user_id, question_id):
        with get_db_connection() as CONN:
            CURSOR = CONN.cursor()
            sql = """
                SELECT *
                FROM user_answers
                WHERE user_id = ? AND question_id = ?
                """
            CURSOR.execute(sql, (user_id, question_id))
            row = CURSOR.fetchone()
            if row:
                user_answer = cls(row[1], row[2], row[3])
                user_answer._user_answer_id = row[0]
                return user_answer
            return None

                  
           