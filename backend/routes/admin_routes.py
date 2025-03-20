from flask import Blueprint, jsonify, request
from backend.services.admin_service import get_all_users
from flask_jwt_extended import jwt_required
from backend.models import db, Subject, Chapter, Quiz, Question, UserQuizAttempt, User
from sqlalchemy import func




admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/users", methods=["GET"])
def list_users():
    users = get_all_users()
    return jsonify(users)


# CREATE Subject
@admin_bp.route('/subject', methods=['POST'])
@jwt_required()
def create_subject():
    data = request.json
    new_subject = Subject(name=data['name'])
    db.session.add(new_subject)
    db.session.commit()
    return jsonify({"message": "Subject created", "subject": new_subject.id}), 201

# READ Subjects
@admin_bp.route('/subjects', methods=['GET'])
@jwt_required()
def get_subjects():
    subjects = Subject.query.all()
    return jsonify([{"id": s.id, "name": s.name} for s in subjects]), 200

# UPDATE Subject
@admin_bp.route('/subject/<int:id>', methods=['PUT'])
@jwt_required()
def update_subject(id):
    data = request.json
    subject = Subject.query.get_or_404(id)
    subject.name = data['name']
    db.session.commit()
    return jsonify({"message": "Subject updated"}), 200

# DELETE Subject
@admin_bp.route('/subject/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_subject(id):
    subject = Subject.query.get_or_404(id)
    db.session.delete(subject)
    db.session.commit()
    return jsonify({"message": "Subject deleted"}), 200


@admin_bp.route('/admin/stats', methods=['GET'])
def get_quiz_stats():
    total_users = db.session.query(func.count(User.id)).scalar()
    total_quizzes = db.session.query(func.count(Quiz.id)).scalar()
    total_attempts = db.session.query(func.count(UserQuizAttempt.id)).scalar()
    
    quiz_performance = (
        db.session.query(Quiz.title, func.avg(UserQuizAttempt.score))
        .join(UserQuizAttempt, UserQuizAttempt.quiz_id == Quiz.id)
        .group_by(Quiz.id)
        .all()
    )
    
    quiz_performance_data = [{"quiz": quiz, "avg_score": avg_score} for quiz, avg_score in quiz_performance]
    
    return jsonify({
        "total_users": total_users,
        "total_quizzes": total_quizzes,
        "total_attempts": total_attempts,
        "quiz_performance": quiz_performance_data
    })