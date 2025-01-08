seed_data = [
    {
        "text": "What is the capital of France?",
        "created_by": 1,
        "choices": [
            {"text": "Paris", "is_correct": True},
            {"text": "London", "is_correct": False},
            {"text": "Berlin", "is_correct": False},
            {"text": "Rome", "is_correct": False},
        ],
    },
    {
        "text": "Who discovered penicillin?",
        "created_by": 1,
        "choices": [
            {"text": "Alexander Fleming", "is_correct": True},
            {"text": "Marie Curie", "is_correct": False},
            {"text": "Louis Pasteur", "is_correct": False},
            {"text": "Gregor Mendel", "is_correct": False},
        ],
    },
    {
        "text": "What is the chemical symbol for water?",
        "created_by": 1,
        "choices": [
            {"text": "H2O", "is_correct": True},
            {"text": "CO2", "is_correct": False},
            {"text": "O2", "is_correct": False},
            {"text": "N2", "is_correct": False},
        ],
    },
    {
        "text": "In which year did World War II end?",
        "created_by": 1,
        "choices": [
            {"text": "1945", "is_correct": True},
            {"text": "1939", "is_correct": False},
            {"text": "1940", "is_correct": False},
            {"text": "1944", "is_correct": False},
        ],
    },
    {
        "text": "What is the square root of 64?",
        "created_by": 1,
        "choices": [
            {"text": "8", "is_correct": True},
            {"text": "6", "is_correct": False},
            {"text": "10", "is_correct": False},
            {"text": "7", "is_correct": False},
        ],
    },
    {
        "text": "Which programming language is primarily used for Android app development?",
        "created_by": 1,
        "choices": [
            {"text": "Java", "is_correct": True},
            {"text": "Python", "is_correct": False},
            {"text": "C++", "is_correct": False},
            {"text": "Swift", "is_correct": False},
        ],
    },
]

from db.models.choices import Choice
from db.models.questions import Question

def seed_questions():
    for data in seed_data:
        existing_question = Question.get_question_by_text(data["text"])
        if not existing_question:
            question = Question(data["text"],data["created_by"])
            question.save()
            print(f"Added question: {data['text']}")

            for choice_data in data["choices"]:
                existing_choice = Choice.get_choices_by_question_id(question.question_id)
                if not any(c.choice_text == choice_data["text"] for c in existing_choice):
                    choice = Choice(question.question_id,choice_data["text"],choice_data["is_correct"])
                    choice.save()
                    print(f" Added choice: {choice_data['text']}")
                else:
                    print(f" Choice already exists: {choice_data['text']}")
         
        else:
            print(f"Question already exists: {data['text']}")
    print("Seeding completed")