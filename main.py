from db.models.questions import Question
from db.models.choices import Choice
from db.models.user_answers import UserAnswer
from db.models.users import User
from seed.seed_data import seed_questions
from auth import register_user, verify_password,hash_password


from colorama import Fore, Style

from lib.helpers import (
    get_user_choice,
    create_questions,
    delete_questions,
    view_all_questions,
    play_trivia
)

def create_tables():

    User.drop_table()
    Question.drop_table()
    UserAnswer.drop_table()
    Choice.drop_table() 
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



def main_menu():
    current_user = None

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

    # Proceed to the main menu for logged-in users
    while True:
        print(Fore.CYAN + f"\nUser: {current_user['username']}  |  Admin Status: {current_user['is_admin']}" + Style.RESET_ALL)
        print(Fore.YELLOW + "\nMain Menu:" + Style.RESET_ALL)

        if current_user['is_admin']:
            options = [
                "Add New Question",
                "Delete Question",
                "View All Questions",
                "Play Trivia",
                "Logout",
                "Exit",
            ]
        else:
            options = [
                "View All Questions",
                "Play Trivia",
                "Logout",
                "Exit",
            ]

        for i, option in enumerate(options):
            print(Fore.GREEN + f"{i}. {option}" + Style.RESET_ALL)

        try:
            choice = int(input(Fore.BLUE + "\nEnter the number corresponding to your choice: " + Style.RESET_ALL))

            if current_user['is_admin']:
                if choice == 0:
                    print("Admin functionality: Add New Question")  # Replace with your function
                elif choice == 1:
                    print("Admin functionality: Delete Question")  # Replace with your function
                elif choice == 2:
                    print("View All Questions")  # Replace with your function
                elif choice == 3:
                    print("Play Trivia")  # Replace with your function
                elif choice == 4:
                    print(Fore.MAGENTA + f"\nLogging you out! Goodbye, {current_user['username']}." + Style.RESET_ALL)
                    return
                elif choice == 5:
                    print(Fore.RED + "\nExiting Trivia App." + Style.RESET_ALL)
                    exit()
                else:
                    print(Fore.RED + "\nInvalid choice. Please try again." + Style.RESET_ALL)
            else:
                if choice == 0:
                    print("View All Questions")  # Replace with your function
                elif choice == 1:
                    print("Play Trivia")  # Replace with your function
                elif choice == 2:
                    print(Fore.MAGENTA + f"\nLogging you out! Goodbye, {current_user['username']}." + Style.RESET_ALL)
                    return
                elif choice == 3:
                    print(Fore.RED + "\nExiting Trivia App." + Style.RESET_ALL)
                    exit()
                else:
                    print(Fore.RED + "\nInvalid choice. Please try again." + Style.RESET_ALL)

        except ValueError:
            print(Fore.RED + "\nInvalid input. Please enter a number." + Style.RESET_ALL)


if __name__ == "__main__":
    create_tables()
    seed_questions()
    while True:
        current_user = login()
        if current_user:
            main_menu(current_user)
        else:
            break
