from db.models.questions import Question
from db.models.choices import Choice
from db.models.user_answers import UserAnswer
from db.models.users import User
from seed.seed_data import seed_questions

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


def login():
    while True:
        print("\nWelcome to the login or registration section")
        print("The list of users is shown below both regular and admin, currently there is no encryption")
        users = User.get_all_users()
        if users:
            print("\nCurrent users:")
            for user in users:
                status = "Admin" if user.is_admin else "Regular"
                print(f"-{user.username} ({status})")
        username = input("Enter your username (or 'q' to exit): ").strip()
        if username == 'q':
            print("Exiting the login section, feel free to come back later")
            exit()
        user = User.get_user_by_username(username)
        if user:
            print(f"Welcome back {user.username}! please explore the options below")
            return user
        else:
            print("User not found, do you want to create a new user?: ")
            choice = input("Type 'yes' to create a new account here,'no' to retry or 'q' to leave if this was a mistake: ").strip()
            if choice == 'q':
                return False
            elif choice == 'yes':
                is_admin = input("Do you want to create an admin or a regular user(an admin has priviledges) type 'yes' for ADMIN or 'no' for REGULAR: ").lower()
                is_admin = is_admin == 'yes' #will result to either True or False
                new_user = User(username=username, is_admin=is_admin)
                new_user.save()
                print(f"User '{username}' created successfully")
                return new_user
            else:
                print("Retrying login...")


def check_user_priviledges():
    if len(User.get_all_users()) == 0:
        print("No users found here, we need atleast one admin account")
        username = input("Enter a username for the admin:") 
        while True:
            is_admin = input("This user has to be an amdin type: (yes)").lower()
            if is_admin in ["yes"]:
                is_truly_admin = is_admin == "yes"
                break
            else:
                print("Invalid input. Please enter 'yes'")
        admin_user = User(username,is_truly_admin)
        admin_user.save()
        print(f"Admin User '{username}' has been created successfully")

def main_menu(current_user):
    while True:
        print(f"User:{current_user.username} Admin status:{current_user.is_admin}") 
        options= []
        if current_user.is_admin:
            print("Hello admin\n")
            options = [
                "Add New Question",
                "Delete Question",
                "View All Questions",
                "Play Trivia",
                "Logout",
                "Exit"
                ]
        else:
            print("Hello regular user\n")
            options = [
                "View All Questions",
                "Play Trivia",
                "Logout",
                "Exit"
               ]
        
        choice = get_user_choice(options)
        if current_user.is_admin:
            if choice == 0:
                create_questions(current_user.user_id) 
            elif choice == 1:
                delete_questions()
            elif choice == 2:
                view_all_questions()
            elif choice == 3:
                play_trivia(current_user.user_id)
            elif choice == 4:
                print(f"Logging you out! godbye {current_user.username}")
                return
            elif choice == 5:
                print("Exiting Trivia App.")
                exit()
        else:
            if choice == 0:
                view_all_questions()
            elif choice == 1:
                play_trivia(current_user.user_id)
            elif choice == 2:
                print(f"Logging you out! godbye {current_user.username}")
                return
            elif choice == 3:
                print("Exiting Trivia App.")
                exit()
        
if __name__ == "__main__":
    create_tables() 
    seed_questions()
    check_user_priviledges()
    while True:
        current_user = login()
        if current_user:
            main_menu(current_user)
        else:
            break
