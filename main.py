from db.models.questions import Question
from db.models.choices import Choice
from db.models.user_answers import UserAnswer
from db.models.users import User
from functions.menu_functions import display_menu, handle_menu_choice
from functions.user_functions import login,ensure_admin_exists
from seed.seed_data import seed_questions
from auth import register_user
from lib.helpers import get_user_choice
from colorama import Fore, Style
from auth import register_user, verify_password
def create_tables():


    User.create_table()
    Question.create_table()
    UserAnswer.create_table()
    Choice.create_table()
def authentication_menu():
    """Handle user registration, login and exit"""
    while True:
        print(Fore.YELLOW + "\nWelcome to the trivia app!" + Style.RESET_ALL)
        print(Fore.GREEN + "1. Register a new User" + Style.RESET_ALL)
        print(Fore.GREEN + "2. Log in" + Style.RESET_ALL)
        print(Fore.GREEN + "3. Exit" + Style.RESET_ALL)

        try:
            choice = int(input(Fore.BLUE + '\nEnter Your choice: ' + Style.RESET_ALL))
            if choice == 1:
                username = input(Fore.BLUE + "Enter a username: " + Style.RESET_ALL).strip()
                password = input(Fore.BLUE + "Enter a password: " + Style.RESET_ALL).strip()
                register_user(username,password)
            elif choice == 2:
                username = input(Fore.BLUE + "Enter your username: " + Style.RESET_ALL).strip()
                password = input(Fore.BLUE + "Enter your password: " + Style.RESET_ALL).strip()
                if verify_password(username, password):
                    print(Fore.GREEN + f"Login successful! Welcome, {username}!" + Style.RESET_ALL)
                    return User.get_user_by_username(username)  
                else:
                    print(Fore.RED + "Login failed. Incorrect username or password." + Style.RESET_ALL)
            elif choice == 3:
                print(Fore.MAGENTA + "Exiting the app. Goodbye!" + Style.RESET_ALL)
                return None
            else:
                print(Fore.RED + "Invalid choice. Please select a valid option. " + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Invalid input, please enter a number" + Style.RESET_ALL())