
from db import get_db_connection
class Question:
    def __init__(self,question_text,created_by,category):
        self._question_id = None
        self.question_text = question_text
        self.created_by = created_by
        self.category = category
    @property
    def category(self):
        return self._category
    @category.setter
    def category(self,category):
        if not isinstance(category,str):
            raise ValueError("Category shdould be a string")
        self._category = category
    @property
    def question_id(self):
        return self._question_id

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
                category TEXT,
                FOREIGN KEY (created_by) REFERENCES users(user_id)
                )
            """
            CONN.execute(sql)
    def save(self):
        with get_db_connection() as CONN:
            CURSOR = CONN.cursor()
            if self._question_id is None:
                sql = """
                    INSERT INTO questions (question_text, created_by,category) VALUES (?, ?,?)
                """
                CURSOR.execute(sql, (self.question_text, int(self.created_by),self.category ))
                self._question_id = CURSOR.lastrowid
            else:
                sql = """
                    UPDATE questions SET question_text = ?, created_by = ?, category = ? WHERE question_id = ?
                """
                CURSOR.execute(sql, (self.question_text, self.created_by,self.category, self._question_id))
    @classmethod
    def get_all_questions(cls):
        with get_db_connection() as CONN:
            CURSOR = CONN.cursor()
            sql = "SELECT * FROM questions"
            rows = CURSOR.execute(sql).fetchall()
            questions = []
            for row in rows:
                question = cls(row[1], int(row[2]))  
                question._question_id = row[0]  
                questions.append(question)
            
            return questions
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
        from db.models.choices import Choice
        if self._question_id == None:
            raise ValueError("this question currently does not exist in the database")
        choices = Choice.get_choices_by_question_id(self._question_id)
        if choices:
            for choice in choices:
                choice.delete()
        else:
            print("No choices associated with this question, something seems off here...")

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
    @classmethod
    def get_questions_by_category(cls,category):
        with get_db_connection() as CONN:
            CURSOR = CONN.cursor()
            sql = """
            SELECT * FROM questions WHERE category = ?
            """
            rows = CURSOR.execute(sql,(category,)).fetchall()
            questions = []
            for row in rows:
                question = cls(row[1],row[2],row[3]) #row 3 is a category
                question._question_id = row[0]
                questions.append(question)
            return questions
    @classmethod
    def display_questions_by_category(cls):
        with get_db_connection() as CONN:
            CURSOR = CONN.cursor()
            sql = "SELECT DISTINCT category FROM questions"
            categories = CURSOR.execute(sql).fetchall()
            for category in categories:
                print(f"Category:{category[0]}")
                questions = cls.get_questions_by_category(category[0])
                for question in questions:
                    print(f" - {question.question_text}")
    
    @classmethod
    def get_question_by_text(cls,text):
        with get_db_connection() as CONN:
            CURSOR = CONN.cursor()
            sql = """
                SELECT * FROM questions WHERE question_text = ?
                    """
            row = CURSOR.execute(sql,(text,)).fetchone()
            if row:
                question = cls(row[1],row[2],row[3])
                question._question_id = row[0]
                return question
            return None