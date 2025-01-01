from lib.helpers import (
    create_questions,
    delete_questions,
    view_all_questions,
    play_trivia
)

def display_menu(user):
    """Display menu options based on user role."""
    options=[
        "View all questions",
        "Play trivia",
        "Logout",
        "Exit"
    ]
    
    adminOptions = ["Add new question", "Delete question"] + options
    return adminOptions if user.is_admin else options
def exit_main_menu():
    # Function to handle exiting the main menu
    raise StopIteration

def handle_menu_choice(choice,user):
    """Handle user menu choices"""
    admin_actions = {
        0:lambda:create_questions(user.user_id),
        1:delete_questions
    }
    common_actions = {
        0:view_all_questions,
        1:lambda:play_trivia(user.user_id),
        2:lambda:(print(f"Logging out {user.username}"), exit_main_menu()),
        3:lambda:exit("exiting the trivia app")
    }
    if user.is_admin:
        if choice in admin_actions:
            admin_actions[choice]()
        else:
            common_actions[choice -2]()
    else:
        common_actions[choice]()