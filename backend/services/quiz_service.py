from backend.models import Quiz, Question, UserQuizAttempt
from backend.database import db

def create_quiz(data):
    quiz = Quiz(title=data["title"], description=data["description"])
    db.session.add(quiz)
    db.session.commit()
    return {"message": "Quiz created successfully", "quiz_id": quiz.id}

def get_quiz_questions(quiz_id):
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    return [{"id": q.id, "text": q.text} for q in questions]

def submit_quiz_attempt(data):
    attempt = UserQuizAttempt(
        user_id=data["user_id"], quiz_id=data["quiz_id"], score=data["score"]
    )
    db.session.add(attempt)
    db.session.commit()
    return {"message": "Quiz attempt recorded"}
