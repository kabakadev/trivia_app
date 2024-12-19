from db.models.questions import Question
from db.models.choices import Choice
from db.models.user_answers import UserAnswer
from db.models.users import User

def check_user_priviledges():
    if User.get_all_users() is None:
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
def main_menu():
    while True:
        username = input("Enter your username: ")
        current_user = User.get_user_by_username(username)
        if current_user is None:
            print("Username not found, we will create a new user...")
            is_admin_input = input("Is this user an admin? (yes/no): ").lower()
            if is_admin_input in ["yes", "no"]:
                is_admin = is_admin_input == "yes"

            else:
                print("Invalid input. Please enter 'yes' or 'no'.")
            local_or_admin_user = User(username, is_admin)
            local_or_admin_user.save()
            print(f"User '{username}' created successfully!")