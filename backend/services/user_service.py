from backend.models import UserQuizAttempt

def get_user_dashboard_data(user_id):
    attempts = UserQuizAttempt.query.filter_by(user_id=user_id).all()
    return [{"quiz_id": a.quiz_id, "score": a.score} for a in attempts]
