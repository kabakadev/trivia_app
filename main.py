from db.models.questions import Question
from db.models.choices import Choice
from db.models.user_answers import UserAnswer
from db.models.users import User
from functions.menu_functions import display_menu, handle_menu_choice
from functions.user_functions import login, ensure_admin_exists
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
                register_user()
            elif choice == 2:
                user = login()
                if user:
                    return user
            elif choice == 3:
                print(Fore.MAGENTA + "Exiting the app. Goodbye!" + Style.RESET_ALL)
                return None
            else:
                print(Fore.RED + "Invalid choice. Please select a valid option. " + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Invalid input, please enter a number" + Style.RESET_ALL())
def main_menu(user):
    """Display the main menu for logged-in users and handle their choices."""
    try:
        while True:
            print(Fore.CYAN + f"\nUser: {user.username} | Status: {'Admin' if user.is_admin else 'Regular'}" + Style.RESET_ALL)
            print(Fore.YELLOW + "\nMain Menu:" + Style.RESET_ALL)
            options = display_menu(user)
            choice = get_user_choice(options)
            handle_menu_choice(choice, user)
    except StopIteration:
        print(Fore.RED + "Returning to the login screen..." + Style.RESET_ALL)


if __name__ == "__main__":
    create_tables()
    ensure_admin_exists()

   
    while True:
        user = authentication_menu()
        if user:
            main_menu(user)
        else:
            break