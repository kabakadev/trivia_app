from db.models.questions import Question
from db.models.choices import Choice
from db.models.user_answers import UserAnswer
from db.models.users import User
from functions.menu_functions import display_menu, handle_menu_choice
from functions.user_functions import login,ensure_admin_exists
from seed.seed_data import seed_questions
from auth import register_user, verify_password,hash_password


from colorama import Fore, Style

from lib.helpers import (
    get_user_choice,
)

def create_tables():


    User.create_table()
    Question.create_table()
    UserAnswer.create_table()
    Choice.create_table() 

def main_menu(user):
    """main menu for logged-in users"""
    try:
        while True:
            print(f"\nUser: {user.username} | Status:{'admin' if user.is_admin else 'regular'}")
            options = display_menu(user)
            choice = get_user_choice(options)
            handle_menu_choice(choice,user)
    except StopIteration:
        print("Returning to login screen...")
if __name__ == "__main__":
    create_tables() 
    # seed_questions()
    ensure_admin_exists()
    while True:
        user_log = login()
        if user_log:
            main_menu(user_log)
        else:
            break
