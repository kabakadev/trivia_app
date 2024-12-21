from db.models.questions import Question
from db.models.choices import Choice
from db.models.user_answers import UserAnswer

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.panel import Panel
from rich.prompt import IntPrompt
from rich.table import Table
import time

console = Console()
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



#refactored code to use timers and colors
console = Console()

def play_trivia(current_user_id):
    console.print(Panel("[bold magenta]Let's play trivia![/bold magenta]", style="blue"))
    
    # Get questions by category
    categories = Question.get_all_categories()
    console.print("[bold cyan]Choose a category:[/bold cyan]")
    for idx, category in enumerate(categories, start=1):
        console.print(f"[bold yellow]{idx}. {category}[/bold yellow]")
    selected_category = IntPrompt.ask(
        "[bold green]Enter the category number[/bold green]", choices=[str(i) for i in range(1, len(categories) + 1)]
    )
    category = categories[selected_category - 1]
    questions = Question.get_questions_by_category(category)
    
    if not questions:
        console.print("[bold red]No questions available in this category![/bold red]")
        return
    
    # Ask how many questions to play
    max_questions = len(questions)
    num_questions = IntPrompt.ask(
        f"[bold green]How many questions would you like to answer? (1-{max_questions})[/bold green]", 
        choices=[str(i) for i in range(1, max_questions + 1)]
    )
    questions = questions[:num_questions]

    # Initialize game
    score = 0
    with Progress(
        SpinnerColumn(),
        BarColumn(),
        TextColumn("[bold blue]{task.description}[/bold blue]"),
        transient=True
    ) as progress:
        task = progress.add_task("Starting trivia...", total=len(questions))
        
        for question in questions:
            console.print(
                Panel(
                    f"[bold yellow]Question:[/bold yellow] {question.question_text}",
                    style="blue",
                )
            )
            choices = Choice.get_choices_by_question_id(question._question_id)
            if not choices:
                console.print("[bold red]No choices available for this question, skipping...[/bold red]")
                progress.advance(task)
                continue
            
            # Display choices
            for idx, choice in enumerate(choices, start=1):
                console.print(f"[cyan]{idx}. {choice.choice_text}[/cyan]")
            
            # Add a countdown timer for urgency
            countdown_timer(10)  # 10-second timer
            
            # Get user input
            selected_index = IntPrompt.ask(
                "[bold green]Select your answer (1-4):[/bold green]",
                choices=[str(i) for i in range(1, len(choices) + 1)]
            ) - 1
            selected_choice = choices[selected_index]

            # Save the user's answer
            user_answer = UserAnswer(
                user_id=current_user_id,
                question_id=question._question_id,
                choice_id=selected_choice._choice_id
            )
            user_answer.save()

            # Provide feedback
            if selected_choice.is_correct:
                console.print("[bold green]Correct![/bold green] :thumbs_up:")
                score += 1
            else:
                console.print("[bold red]Incorrect! Better luck next time![/bold red] :thumbs_down:")
            
            console.print("-" * 20)
            progress.advance(task)
    
    # Display results
    display_results(score, len(questions))

def countdown_timer(seconds):
    for i in range(seconds, 0, -1):
        console.print(f"[bold red]{i}[/bold red] seconds remaining...", end="\r")
        time.sleep(1)
    console.print("[bold red]Time's up![/bold red]")

def display_results(score, total):
    table = Table(title="Trivia Results", style="green")
    table.add_column("Score", justify="center", style="bold yellow")
    table.add_column("Total Questions", justify="center", style="bold cyan")
    table.add_row(str(score), str(total))
    console.print(table)

