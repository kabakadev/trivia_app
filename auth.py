import bcrypt
from db import get_db_connection
from db.models.users import User
from colorama import Fore, Style
# Hashes a plaintext password
def hash_password(password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

# Verifies a plaintext password against a stored hash
def verify_password(username, password):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # Fetch the stored password hash for the user
        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()

        if row is None:
            print("User not found.")
            return False

        stored_hash = row[0]
        return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))

# Registers a new user in the database
def register_user():
    """
    Registers a new user by prompting for username and password.
    """
    username = input(Fore.BLUE + "Enter a username: " + Style.RESET_ALL).strip()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # Check if the username already exists
        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        if cursor.fetchone() is not None:
            print("Username already taken. Please choose a different username.")
            return None

    password = input(Fore.BLUE + "Enter a password: " + Style.RESET_ALL).strip()
    hashed_password = hash_password(password)  # Hash the password

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password)
        )
        print(f"User {username} registered successfully!")
        return User.get_user_by_username(username)  # Return the newly created user
def login():
    """
    Handles user login.
    Returns a User object if login is successful, otherwise None.
    """
    while True:
        print("\nWelcome to the login section.")
        username = input("Enter your username (or 'q' to exit): ").strip()
        
        if username.lower() == 'q':
            print("Exiting the login section. Feel free to come back later.")
            return None

        user = User.get_user_by_username(username)
        if user:
            password = input("Enter your password: ").strip()
            if verify_password(username, password):
                print(f"Login successful! Welcome, {user.username}.")
                return user
            else:
                print("Incorrect password. Please try again.")
        else:
            print("User not found.")
            retry = input("Would you like to retry? Type 'yes' to retry or 'no' to exit: ").strip().lower()
            if retry == 'no':
                return None
