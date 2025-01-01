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


def main_menu(user):
    """main menu for logged-in users"""
    while True:
        print(Fore.YELLOW + "\nWelcome to the Trivia App!" + Style.RESET_ALL)
        print(Fore.GREEN + "1. Register a New User" + Style.RESET_ALL)
        print(Fore.GREEN + "2. Log In" + Style.RESET_ALL)
        print(Fore.GREEN + "3. Exit" + Style.RESET_ALL)

        try:
            choice = int(input(Fore.BLUE + "\nEnter your choice: " + Style.RESET_ALL))

            if choice == 1:
                # Registration
                username = input(Fore.BLUE + "Enter a username: " + Style.RESET_ALL)
                password = input(Fore.BLUE + "Enter a password: " + Style.RESET_ALL)
                register_user(username, password)

            elif choice == 2:
                # Login
                username = input(Fore.BLUE + "Enter your username: " + Style.RESET_ALL)
                password = input(Fore.BLUE + "Enter your password: " + Style.RESET_ALL)
                if verify_password(username, password):
                    print(Fore.GREEN + f"Login successful! Welcome, {username}!" + Style.RESET_ALL)
                    current_user = {"username": username, "is_admin": username == "admin"}  # Example admin logic
                    break
                else:
                    print(Fore.RED + "Login failed. Incorrect username or password." + Style.RESET_ALL)

            elif choice == 3:
                # Exit
                print(Fore.MAGENTA + "Exiting the app. Goodbye!" + Style.RESET_ALL)
                return

            else:
                print(Fore.RED + "Invalid choice. Please select a valid option." + Style.RESET_ALL)

        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a number." + Style.RESET_ALL)

    try:
        while True:
            print(f"Fore.CYAN + \nUser: {user.username} | Status:{'admin' if user.is_admin else 'regular'}")
            print(Fore.YELLOW + "\nMain Menu:" + Style.RESET_ALL)
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
