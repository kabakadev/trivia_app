from db.models.questions import Question
from db.models.choices import Choice
from db.models.user_answers import UserAnswer
from db.models.users import User

def check_user_priviledges():
    if User.get_all_users() is None:
        print("No users found here, we need atleast one admin account")
        while True:
            username = input("Enter a username for the admin:")
            try:
                User.get_user_by_username(username)
                print("Username found, try a new one")
            except:
                break
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
