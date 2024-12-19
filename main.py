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

def get_user_choice(options):
    print("\nPlease choose an option:")
    for index, option in enumerate(options):
        print(f"{index}. {option}")
    while True:
        try:
            choice = int(input("Enter the number corresponding to your choice: "))
            if 0 <= choice < len(options):
                return choice
            else:
                print(f"Invalid choice. Please enter a number between 0 and {len(options) - 1}.")
        except ValueError:
            print("Invalid input. Please enter a number.")
def create_questions(admin_user_id):
    print('\nAdd a new question')
    question_text = input("Enter the question text: ").strip()
    if not question_text:
        print("Question text cannot be empty")
        return
    question = Question(question_text, admin_user_id)
    question.sve()

    print("Now, let's add multiple-choice options for this question")
    choices = []

    for i in range(4): #each question will be constrained to only 4 multiple choices
        choice_text = input(f"Enter choice{i + 1}: ").strip()
        is_correct = input("Is this the correct answer? (yes/no): ").lower() == "yes"
        choice = Choice(question._question_id,choice_text,is_correct)
        choices.append(choice)
    for choice in choices:
        choice.save()
    print(f"Question '{question_text}' with choices has been added successfully ")


def delete_questions():
    print("Fetching all questions ...\n")
    questions = Question.get_all_questions()
    if not questions:
        print("No question available to delete")
        return
    print("Available Questions")
    for question in questions:
        print(f"{question._question_id}:{question.question_text}")
    while True:
        try:
            question_id = int(input("\nEnter the ID of the question you want to delete (or 0 to cancel): "))
            if question_id == 0:
                print("Delete operation cancelled.")
                return
            question_to_delete = Question.get_question_by_id(question_id)
            if question_to_delete is None:
                print("Invalid question ID. Please try again.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a valid question ID.")
    confirm = input(f"Are you sure you want to delete the question: '{question_to_delete.question_text}'? (yes/no): ").lower()
    if confirm == "yes":
        question_to_delete.delete()
        print("question deleted successfully")
    else:
        print("You have cancelled this deleting operation and the question is not deleted")

def main_menu():
    while True:
        print("\nMain Menu:")
        print("Type 'q' to quit or exit")
        username = input("Enter your username or type q to quit: ")
        if username.lower() == 'q':
            print("The program has stopped, hoping to see you again!")
            break
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
        else:
            print(f"Welcome back, {current_user.username} Admin status:{current_user.is_admin}") 
      
        options= []
        if current_user.is_admin:
            print("Hello admin\n")
            options = [
                "\nAdd New Question",
                "\nDelete Question",
                "\nView All Questions",
                "\nPlay Trivia",
                "\nExit"
                ]
        else:
            print("Hello regular user\n")
            options = [
                "\nView All Questions",
                "\nPlay Trivia",
                "\nExit"
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
                print("This feature is not yet implemented.")
            elif choice == 4:
                print("Exiting Trivia App.")
                break
        else:
            if choice == 0:
                view_all_questions()
            elif choice == 1:
                print("This feature is not yet implemented.")
            elif choice == 2:
                print("Exiting Trivia App.")
                break
        
        print("Invalid choice. Please try again.")