import bcrypt
from db import get_db_connection

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

        conn.close()

        if row is None:
            print("User not found.")
            return False

        stored_hash = row[0]
        return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))

# Registers a new user in the database
def register_user(username, password):
     with get_db_connection() as conn:
        cursor = conn.cursor()
    # Check if the username already exists
        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        if cursor.fetchone() is not None:
            print("Username already taken.")
            conn.close()
            return

        # Hash the password and store the user
        hashed_password = hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password)
        )
        print(f"User {username} registered successfully!")
