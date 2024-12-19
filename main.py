from db.models.questions import Question
from db.models.choices import Choice
from db.models.user_answers import UserAnswer
from db.models.users import User


def create_tables():
    User.drop_table()
    Question.drop_table()
    UserAnswer.drop_table()
    Choice.drop_table()

    User.create_table()
    Question.create_table()
    UserAnswer.create_table()
    Choice.create_table()


    



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
    question.save()

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
def view_all_questions():
    print("fetching questions...")
    questions = Question.get_all_questions()

    if not questions:
        print("No questions availabel")
        return
    print("trivia questions:\n")
    for question in questions:
        print(f"Question ID {question._question_id} : {question.question_text}")
        choices = Choice.get_choices_by_question_id(question.question_id)
        if choices:
            for index,choice in enumerate(choices,start =1):
                print(f"   {index}, {choice.choice_text}")
        else:
            print("   No choices available for this question which is weird, each question must contain choices")
        print("-" * 20)
def play_trivia(current_user_id):
    print("\nLet's play trivia! \n")
    questions = Question.get_all_questions()
    if not questions:
        print("No questions available for trivia. which is weird, I will look into it.")
        return
    score = 0
    for question in questions:
        print(f"Question: {question.question_text}")
        choices = Choice.get_choices_by_question_id(question._question_id)
        if not choices:
            print("No choices available for this question, which is weird again and should not be happening. skipping...")
            continue
        for index,choice in enumerate(choices,start=1):
            print(f"{index}.{choice.choice_text}")
        while True:
            try:
                selected_index = int(input("Select Your answer (1-4): ")) -1
                if 0 <= selected_index <len(choices):
                    break
                else:
                    print("Invalid Choice. please select a valid option")
            except ValueError:
                print("Invalid input. Please enter a number")
        selected_choice = choices[selected_index]

        user_answer = UserAnswer(
            user_id=current_user_id,
            question_id=question._question_id,
            choice_id=selected_choice._choice_id
        )
        user_answer.save()

        if selected_choice.is_correct:
            print("Correct!! ")
            score +=1
        else:
            print("Incorrect, better luck next time!")
        print("-" * 20)
    print(f"You have completed the trivia! your total score is: {score}/{len(questions)}")

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
            current_user = local_or_admin_user
        else:
            print(f"Welcome back, {current_user.username} Admin status:{current_user.is_admin}") 
      
        options= []
        if current_user.is_admin:
            print("Hello admin\n")
            options = [
                "Add New Question",
                "Delete Question",
                "View All Questions",
                "Play Trivia",
                "Exit"
                ]
        else:
            print("Hello regular user\n")
            options = [
                "View All Questions",
                "Play Trivia",
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
                print("Exiting Trivia App.")
                break
        else:
            if choice == 0:
                view_all_questions()
            elif choice == 1:
                play_trivia(current_user.user_id)
            elif choice == 2:
                print("Exiting Trivia App.")
                break
        
        print("Invalid choice. Please try again.")
if __name__ == "__main__":
    create_tables() 
    check_user_priviledges()
    main_menu()