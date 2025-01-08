from db.models.users import User
def display_users():
    """display a list of uders"""
    users = User.get_all_users()
    if users:
        print("\nCurrent users:")
        for user in users:
            status = "Admin" if user.is_admin else "Regular"
            print(f"-{user.username} ({status}) ")
    else:
        print("No users have been created at the moment.")
def prompt_user_input(prompt,valid_options=None):
    """Helper function to get validated user input"""
    while True:
        user_input = input(prompt).strip().lower()
        if valid_options is None or user_input in valid_options:
            return user_input
        print(f"Invalid input. Please enter one of: {', '.join(valid_options)}")

def login():
    while True:
        print("\nLogin / Registration")
        display_users()

        username = input("Enter your username(or 'q' to exit): ").strip()
        if username == 'q':
            print("Exiting the login section.")
            return None
        if len(username) < 3:
            print("username must have 3 characters or more")
            continue
        if not username.isalnum():
            print ("username must contain only alphanumeric characters")
            continue
        if username.isdigit():
            print("username cannot contain only numbers")
            continue
        if not username:
            print("username cannot be empty")
            continue
      
        
        user = User.get_user_by_username(username)
        if user:
            print(f"Welcome back, {user.username}!")
            return user
        print("User not founf. Would you like to create a new user?")
        choice = prompt_user_input(
            "Type 'yes' to create, 'no' to retry, or 'q' to quit: ",
            valid_options=['yes','no','q']
        )
        if choice == 'q':
            return None
        elif choice == 'yes':
            is_admin = prompt_user_input(
                "Create an Admin? Type 'yes' for Admin, 'no' for Regular: ",
                valid_options=['yes','no']
            ) == 'yes'
            new_user = User(username=username, is_admin=is_admin)
            new_user.save()
            print(f"User, '{username}' created successfully.")
            return new_user
def ensure_admin_exists():
    """make sure that we have atleast one admin"""
    if not User.get_all_users():
        print("No users found. Creating an admin account.")
        username = input("Enter a username for the admin: ").strip()
        admin_user = User(username=username, is_admin=True)
        admin_user.save()
        print(f"Admin user '{username}' created successfully.")
