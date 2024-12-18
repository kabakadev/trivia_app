from db_connection import get_db_connection
class Choice:
    def __init__(self,question_id,choice_text,is_correct):
        self._choice_id = None
        self._question_id = question_id
        self._choice_text = choice_text
        self._is_correct = is_correct
    @property
    def question_id(self):
        return self._question_id
    @question_id.setter
    def question_id(self, question_id):
        if not isinstance(question_id, int):
            raise ValueError("the question id must be an integer")
        self._question_id = question_id
    @property
    def choice_text(self):
        return self._choice_text

    @choice_text.setter
    def choice_text(self, choice_text):
        if not isinstance(choice_text, str):
            raise ValueError("choice text must be a string")
        self._choice_text = choice_text
    @property
    def is_correct(self):
        return self._is_correct

    @is_correct.setter
    def is_correct(self, is_correct):
        if not isinstance(is_correct, bool):
            raise ValueError("is correct must be a boolean either true or false")
        self._is_correct = is_correct