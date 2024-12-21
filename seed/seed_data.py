from db.models.questions import Question
questions = [
    {"text": "What is the capital of France?", "created_by": 1, "category": "Geography"},
    {"text": "Who discovered penicillin?", "created_by": 1, "category": "Science"},
    {"text": "What year did the Titanic sink?", "created_by": 1, "category": "History"},
    {"text": "Who won the first Academy Award for Best Actor?", "created_by": 1, "category": "Entertainment"},
]
def seed_questions():
    for q in questions:
        question = Question(q["text"], q["created_by"], q["category"])
        existing_question = Question.get_question_by_text(q["text"])  # Add a method to check for duplicates
        if not existing_question:
            question.save()
    print("Seeding completed.")