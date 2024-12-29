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

def display_users():
    """display a list of uders"""
    users = User.get_all_users()
    if users:
        print("\nCurrent users:")
        for user in users:
            status = "Admin" if user.is_admin else "Regular"
            print(f"-{user.username} ({status}) ")
    else:
        print("No users have been created at the moment.")
