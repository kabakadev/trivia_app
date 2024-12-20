# Trivia CLI Application

## Author

**Ian Kabaka**

---

## Title

**Trivia CLI Application**

---

## Project Description

The Trivia CLI Application is an interactive command-line tool designed for creating and playing trivia quizzes. The application supports user roles with different privileges: administrators and regular users. Administrators can manage questions (add,delete) and control the flow of the trivia quizzes, while regular users can participate by answering questions. The application stores data persistently using SQLite3 and ensures a smooth user experience with robust input handling and role-based access control.

---

## Project Features

### User Roles

1. **Admin Role**:

   - Can create, view, update, and delete trivia questions.
   - Has full control over question sets and the structure of the trivia game.

2. **Regular User Role**:
   - Can view available trivia questions.
   - Can play the trivia game by answering multiple-choice questions.

### Features

- **Role-Based Menus**: Separate menus and functionalities based on user roles.
- **Question Management**: Administrators can create and delete questions from the trivia database.
- **Trivia Gameplay**: Regular users can answer question and view results and score based on what they got right or wrong.
- **Persistent Storage**: Data is stored in a SQLite3 database for reliability and persistence.
- **User Authentication**: Users can log in by selecting an existing username or create a new account.
- **Exit Options**: Users can exit the program at any point for convenience.

---

## How to Get Started

### Prerequisites

- Python 3.7+
- SQLite3, this comes standard with the current python version above or the latest python installation .

### Installation Steps

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/kabakadev/trivia_app.git
   ```

2. **cd into the directory**:

```bash
  cd trivia_app
```

3. **Install Dependencies**:

   This project does not have external dependencies outside the Python standard library. Ensure you have Python 3.8+ installed.
   You can use pip to target the exact version of the current python used in this project which is Python 3.8.13 or installing the latest version of python from the python.org website.

4. **Run the Application**:

   Run the following command to start the program:

   ```bash
   python main.py
   ```

   The program will automatically create all required tables.

## Usage

### Login Process

1. Upon starting the application, you will see a list of existing users along with their roles (Admin/Regular User).
2. Choose to either log in with an existing username, create a new account, or exit the program.

### Admin Menu

Admins can:

- Add new trivia questions.
- Edit existing questions.
- Delete questions.
- View all questions.

### Regular User Menu

Regular users can:

- View questions (read-only).
- Play the trivia game and answer questions.

### Exit Option

Users can exit the program at any point.

#### Check user priviledges

This program can only be used when there is an admin account, when there is no user or an admin in the database, a different
prompt for creating an admin will be shown, this is a rare occurence that can happen if any updates happen and the tables
created at the point of this program iteration are dropped, I will take measures to ensure that does not happen.

#### Login/Registration Prompt

- **Current Users**:When you enter the application for the first time,it displays a list of existing users and their roles (Admin/Regular User).
- **Login**: Enter your username to log in.You can pick it from the list of the Current users shown above the username prompt.

- **Create New User**:If for any reasons your name is not shown in Current users, you can enter a new username to create an account.

- **Revert actions**: you can revert any actions during the creation of your user, and either exit the program by pressing 'q' or you can press 'no' to retry this entire process.

- **Quit**: Type 'q' to the username input field to exit the program. This is the only key word and should not be used when creating a user.
- **Super user priviledges**: in here you can choose to create an accunt as an admin or as a regular user.
  - An admin has extra priviledges like creating questions and deleting them and more to come in future updates,
  - A regular user can just view the questions and play the trivia game

#### Admin Menu Options

In here the admin can type any of the numbers displayed before each menu to select the menu options

- **0. Add New Question**: Allows the admin to create a new trivia question and save it to the database. The admin can type 0 or leave it blank to go back to the main menu.

  - However if they choose to type a question, they will be prompted for the options to this question and their corresponding correctness, if they enter an option, they can decide if that option is correct or not, by typing 'yes' or 'no'.

  - Each question by convention can only have one answer but this is for the admin to decide, the options are limited to four for each question.

- **1. Delete Question**: Fetches all questions and enables the admin to delete a specific question by its ID.The admin can type 0 to cancel this process.

  - The ID of the question is the number that appears before the semicolon(:) e.g 1:Which is the most fastest car in the world? (1) will be the ID of that question.
  - if the admin picks it, he/she will be prompted again and can type 'yes' or 'no' to confirm that action, if they type yes, then the question will be deleted, if they type no then they will go back to the main menu

- **2. View All Questions**: Displays all questions in the database, including their multiple-choice answers.After the questions are shown, they will be automatically be taken back to the main menu.

- **3. Play Trivia**: Allows the admin to play the trivia game.

  - When user answers each question which is turn based, they willl get feedback wether the answer they gave is correct or false, answering the question is by number based, the user can select the answer by entering a number (1-4 ) each number corresponding to the option being chosen.

- **4. Logout**: Logs out the current admin and returns to the login/registration prompt.
- **5. Exit**: Exits the program.

#### Regular User Menu Options

In here a regular user can choose any of the numbers displayed before each menu to select the menu optons

- **0. View All Questions**: Displays all questions in the database, including their multiple-choice answers.
- **1. Play Trivia**: Starts the trivia game for the user to answer questions and track their score.

  - When user answers each question which is turn based, they willl get feedback wether the answer they gave is correct or false, answering the question is by number based, the user can select the answer by entering a number (1-4 ) each number corresponding to the option being chosen.

- **2. Logout**: Logs out the current user and returns to the login/registration prompt.
- **3. Exit**: Exits the program.

---

## License

This project is licensed under the MIT License. See below for details:

MIT License

Copyright (c) [2024] Ian Kabaka

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---
