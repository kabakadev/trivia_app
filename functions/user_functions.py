from db.models.users import User
from colorama import Fore, Style
from auth import verify_password,hash_password
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
        print("\nWelcome to the login or registration section")
        print("The list of users is shown below both regular and admin, currently there is no encryption")
        users = User.get_all_users()
        if users:
            print("\nCurrent users:")
            for user in users:
                status = "Admin" if user.is_admin else "Regular"
                print(f"- {user.username} ({status})")
        else:
            print("\nNo users found. Please register a new user.")

        username = input("Enter your username (or 'q' to exit): ").strip()
        if username == 'q':
            print("Exiting the login section, feel free to come back later.")
            return None

        user = User.get_user_by_username(username)
        if user:
            password = input("Enter your password: ").strip()
            if verify_password(user.password, password):
                print(f"Welcome back, {user.username}! Please explore the options below.")
                return user
            else:
                print("Incorrect password. Please try again.")
        else:
            print("User not found. Do you want to create a new user?")
            choice = input("Type 'yes' to create a new account, 'no' to retry, or 'q' to leave: ").strip().lower()
            if choice == 'q':
                return None
            elif choice == 'yes':
                is_admin = input("Do you want to create an admin or a regular user? Type 'yes' for ADMIN or 'no' for REGULAR: ").strip().lower()
                is_admin = is_admin == 'yes'  # Convert to True/False
                password = input("Enter a password for the new account: ").strip()
                hashed_password = hash_password(password)  # Hash the password
                print(hashed_password)

                new_user = User(username=username, password=hashed_password, is_admin=is_admin)
                new_user.save()

                print(f"User '{username}' created successfully.")
                return new_user
            else:
                print("Retrying login...")



def ensure_admin_exists():
    """make sure that we have atleast one admin"""
    if not User.get_all_users():
        print("No users found. Creating an admin account.")
        username = input("Enter a username for the admin: ").strip()
        admin_user = User(username=username, is_admin=True)
        admin_user.save()
        print(f"Admin user '{username}' created successfully.")
