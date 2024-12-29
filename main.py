from db.models.questions import Question
from db.models.choices import Choice
from db.models.user_answers import UserAnswer
from db.models.users import User

from lib.helpers import (
    get_user_choice,
    create_questions,
    delete_questions,
    view_all_questions,
    play_trivia
)

def create_tables():
    User.create_table()
    Question.create_table()
    UserAnswer.create_table()
    Choice.create_table() 

