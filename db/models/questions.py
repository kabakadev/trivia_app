
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
                created_by INTEGER,
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
    @classmethod
    def get_question_by_id(cls,question_id):
        with get_db_connection() as CONN:
      
            CURSOR = CONN.cursor()
            sql = """
                SELECT *
                FROM questions

                WHERE question_id = ?
                """
            row = CURSOR.execute(sql,(question_id,)).fetchone()
            if row:
                question = cls(row[1], bool(row[2])) 
                question._question_id = row[0] 
                return question
        return None 
    def delete(self):
        if self._question_id == None:
            raise ValueError("this question currently does not exist in the database")
        with get_db_connection() as CONN:
            CURSOR = CONN.cursor()

            sql = """DELETE FROM questions WHERE question_id = ?  """
            CURSOR.execute(sql,(self._question_id,))
            self._question_id = None
    @classmethod
    def drop_table(cls):
       with get_db_connection() as CONN:
            CURSOR = CONN.cursor()

            sql = """DROP TABLE IF EXISTS questions"""
            CURSOR.execute(sql)
Question.drop_table()
print("question table has been dropped")
question1 = Question("who is the president of the USA?",1)
question3 = Question("where is the tallest mountain?",2)
question2 = Question("who has the biggest house in Dubai" ,1)
question1.create_table()

question1.save()
question2.save()
question3.save()
question = question1.get_question_by_id(1)
question_get = question2.get_question_by_id(2)

if question:
    print(f"question found: {question.question_text}")
else:
    print("question not found.")
if question_get:
    print(f"question found: {question_get.question_text}")
else:
    print("question not found.")
        

