from flask import Blueprint, request, jsonify
from backend.services.user_service import get_user_dashboard_data
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import db, Subject, Chapter, Quiz, Question, UserQuizAttempt


user_bp = Blueprint("user", __name__)

@user_bp.route("/dashboard", methods=["GET"])
def dashboard():
    user_id = request.args.get("user_id")
    data = get_user_dashboard_data(user_id)
    return jsonify(data)


@user_bp.route('/quiz/attempt', methods=['POST'])
@jwt_required()
def submit_quiz_attempt():
    data = request.json
    user_id = get_jwt_identity()  # Get user ID from JWT token

    new_attempt = UserQuizAttempt(
        user_id=user_id,
        quiz_id=data['quiz_id'],
        score=data['score']
    )
    db.session.add(new_attempt)
    db.session.commit()

    return jsonify({"message": "Quiz attempt recorded", "score": data['score']}), 201



# Fetching past quiz attempts api
@user_bp.route('/quiz/attempts', methods=['GET'])
@jwt_required()
def get_past_attempts():
    user_id = get_jwt_identity()
    attempts = UserQuizAttempt.query.filter_by(user_id=user_id).all()

    return jsonify([
        {
            "quiz_id": attempt.quiz_id,
            "score": attempt.score,
            "date_taken": attempt.attempt_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        for attempt in attempts
    ])
