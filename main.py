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
def prompt_user_input(prompt,valid_options=None):
    """Helper function to get validated user input"""
    while True:
        user_input = input(prompt).strip().lower()
        if valid_options is None or user_input in valid_options:
            return user_input
        print(f"Invalid input. Please enter one of: {', '.join(valid_options)}")
def login():
    while True:
        print("\nLogin / Registration")
        display_users()

        username = input("Enter your username(or 'q' to exit): ").strip()
        if username == 'q':
            print("Exiting the login section.")
            return None
        user = User.get_user_by_username(username)
        if user:
            print(f"Welcome back, {user.username}!")
            return user
        print("User not founf. Would you like to create a new user?")
        choice = prompt_user_input(
            "Type 'yes' to create, 'no' to retry, or 'q' to quit: ",
            valid_options=['yes','no','q']
        )
        if choice == 'q':
            return None
        elif choice == 'yes':
            is_admin = prompt_user_input(
                "Create an Admin? Type 'yes' for Admin, 'no' for Regular: ",
                valid_options=['yes','no']
            ) == 'yes'
            new_user = User(username=username, is_admin=is_admin)
            new_user.save()
            print(f"User, '{username}' created successfully.")
            return new_user
def ensure_admin_exists():
    """make sure that we have atleast one admin"""
    if not User.get_all_users():
        print("No users found. Creating an admin account.")
        username = input("Enter a username for the admin: ").strip()
        admin_user = User(username=username, is_admin=True)
        admin_user.save()
        print(f"Admin user '{username}' created successfully.")

def display_menu(user):
    """Display menu options based on user role."""
    options=[
        "View all questions",
        "Play trivia",
        "Logout",
        "Exit"
    ]
    
    adminOptions = ["Add new question", "Delete question"] + options
    return adminOptions if user.is_admin else options
def exit_main_menu():
    # Function to handle exiting the main menu
    raise StopIteration

def handle_menu_choice(choice,user):
    """Handle user menu choices"""
    admin_actions = {
        0:lambda:create_questions(user.user_id),
        1:delete_questions
    }
    common_actions = {
        0:view_all_questions,
        1:lambda:play_trivia(user.user_id),
        2:lambda:(print(f"Logging out {user.username}"), exit_main_menu()),
        3:lambda:exit("exiting the trivia app")
    }
    if user.is_admin:
        if choice in admin_actions:
            admin_actions[choice]()
        else:
            common_actions[choice -2]()
    else:
        common_actions[choice]()


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
    ensure_admin_exists()
    while True:
        user = login()
        if user:
            main_menu(user)
