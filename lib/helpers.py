from db.models.questions import Question
from db.models.choices import Choice
from db.models.user_answers import UserAnswer
from rich.console import Console

def create_questions(admin_user_id):
    print('\nAdd a new question')
    question_text = input("Enter the question text (or press type 0 or leave blank to go back to the main menu): ").strip()
    if not question_text:
        print("You did not type anything, you can try again, going back to the main menu...")
        return
    if question_text == '0':
        print("You can try again, going back to the main menu...")
        return
    categories = Question.get_all_categories()
    if categories:
        print("\nHere are the top 5 categories:")
        for i,category in enumerate(categories[:5],start=1):
            print(f"{i}.{category}")
        while True:
            print("\nOptions:")
            print("1. View next 10 categories")
            print("2. View all categories")
            print("3. Skip viewing categories")
            choice = input("Pick an option from above or enter 3 to skip viewing categories: ").strip()

            if choice == "1":
                for i in range(5, len(categories),10):
                    print("\nNext 10 categories:")
                    for category in categories[i:i+10]:
                        print(f"- {category}")
                    cont = input("View more? (yes/no): ").strip().lower()
                    if cont != "yes":
                        break
            elif choice == "2":
                print("\nAll categories")
                for category in categories:
                    print(f" - {category}")
                break
            elif choice == "3":
                break
            else:
                print("Invalid choice try again")
    category = input("Enter the category for this question: ").strip()
    if not category:
        print("Category cannot be left blank. please try again")
        return create_questions(admin_user_id) #recursion nice!
    
    
    question = Question(question_text, admin_user_id,category)
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
            question_id = int(input("\nEnter the ID of the question you want to delete, this ID is the number before the (:) colon before each question text  (or 0 to cancel): "))
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
console = Console()


from colorama import Fore, Style

def play_trivia(current_user_id):
    print(Fore.CYAN + "\nWelcome to the Trivia Game!" + Style.RESET_ALL)

    categories = Question.get_all_categories()
    if not categories:
        print(Fore.RED + "No categories available. Please add questions first." + Style.RESET_ALL)
        return

    print(Fore.YELLOW + "\nAvailable Categories:" + Style.RESET_ALL)
    for idx, category in enumerate(categories, 1):
        print(Fore.GREEN + f"{idx}. {category}" + Style.RESET_ALL)
    print(Fore.GREEN + "0. Exit to Main Menu" + Style.RESET_ALL)

    while True:
        try:
            category_choice = int(input(Fore.BLUE + "\nSelect a category by number: " + Style.RESET_ALL))
            if category_choice == 0:
                return
            if 1 <= category_choice <= len(categories):
                selected_category = categories[category_choice - 1]
                break
            else:
                print(Fore.RED + "Invalid choice. Please select a valid category." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a number." + Style.RESET_ALL)

    questions = Question.get_questions_by_category(selected_category)
    if not questions:
        print(Fore.RED + f"No questions available in the category: {selected_category}." + Style.RESET_ALL)
        return

    while True:
        try:
            num_questions = int(input(Fore.BLUE + f"\nHow many questions would you like to answer? (1-{len(questions)}): " + Style.RESET_ALL))
            if 1 <= num_questions <= len(questions):
                break
            else:
                print(Fore.RED + f"Please enter a number between 1 and {len(questions)}." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a number." + Style.RESET_ALL)

    score = 0
    for idx, question in enumerate(questions[:num_questions], 1):
        print(Fore.YELLOW + f"\nQuestion {idx}/{num_questions}: {question.question_text}" + Style.RESET_ALL)
        choices = Choice.get_choices_by_question_id(question._question_id)
        for i, choice in enumerate(choices, 1):
            print(Fore.GREEN + f"{i}. {choice.choice_text}" + Style.RESET_ALL)

        while True:
            try:
                user_choice = int(input(Fore.BLUE + "\nSelect your answer: " + Style.RESET_ALL)) - 1
                if 0 <= user_choice < len(choices):
                    selected_choice = choices[user_choice]
                    if selected_choice.is_correct:
                        print(Fore.GREEN + "Correct!" + Style.RESET_ALL)
                        score += 1
                    else:
                        print(Fore.RED + "Incorrect!" + Style.RESET_ALL)

                    UserAnswer(
                        user_id=current_user_id,
                        question_id=question._question_id,
                        choice_id=selected_choice._choice_id
                    ).save()

                    break
                else:
                    print(Fore.RED + "Invalid choice. Please select a valid option." + Style.RESET_ALL)
            except ValueError:
                print(Fore.RED + "Invalid input. Please enter a number." + Style.RESET_ALL)

        print(Fore.MAGENTA + "-" * 20 + Style.RESET_ALL)

    print(Fore.CYAN + f"\nYou have completed the trivia! Your total score is: {score}/{num_questions}" + Style.RESET_ALL)
