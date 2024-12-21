from db.models.questions import Question
from db.models.choices import Choice
from db.models.user_answers import UserAnswer

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
            choice = input("Enter your choice: ").strip()

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
