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