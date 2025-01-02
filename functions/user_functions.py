from db.models.users import User
from colorama import Fore, Style
from auth import verify_password
def display_registered_users():
    """display a list of uders"""
    users = User.get_all_users()
    if users:
        print("\nCurrent users:")
        for user in users:
            status = "Admin" if user.is_admin else "Regular"
            print(f"-{user.username} ({status}) ")
    else:
        print("No users have been created at the moment.")

def login():
    """
    Handles user login.
    Returns a User object if login is successful, otherwise None.
    """
    while True:
        print("\nWelcome to the login section.")
        username = input("Enter your username (or 'q' to exit): ").strip()
        
        if username.lower() == 'q':
            print("Exiting the login section. Feel free to come back later.")
            return None

        user = User.get_user_by_username(username)
        if user:
            password = input("Enter your password: ").strip()
            if verify_password(username, password):
                print(f"Login successful! Welcome, {user.username}.")
                return user
            else:
                print("Incorrect password. Please try again.")
        else:
            print("User not found.")
            retry = input("Would you like to retry? Type 'yes' to retry or 'no' to exit: ").strip().lower()
            if retry == 'no':
                return None




def ensure_admin_exists():
    """make sure that we have atleast one admin"""
    if not User.get_all_users():
        print("No users found. Creating an admin account.")
        username = input("Enter a username for the admin: ").strip()
        admin_user = User(username=username, is_admin=True)
        admin_user.save()
        print(f"Admin user '{username}' created successfully.")
