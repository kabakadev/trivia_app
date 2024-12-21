seed_data = [
    {
        "text": "What is the capital of France?",
        "created_by": 1,
        "category": "Geography",
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
        "category": "Science",
        "choices": [
            {"text": "Alexander Fleming", "is_correct": True},
            {"text": "Marie Curie", "is_correct": False},
            {"text": "Louis Pasteur", "is_correct": False},
            {"text": "Gregor Mendel", "is_correct": False},
        ],
    },
]
from db.models.choices import Choice
from db.models.questions import Question

def seed_questions():
    for data in seed_data:
        existing_question = Question.get_question_by_text(data["text"])
        if not existing_question:
            question = Question(data["text"],data["created_by"],data["category"])
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