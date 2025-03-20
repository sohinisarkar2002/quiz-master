from flask import Blueprint, request, jsonify
from backend.services.quiz_service import create_quiz, get_quiz_questions, submit_quiz_attempt

quiz_bp = Blueprint("quiz", __name__)

@quiz_bp.route("/create", methods=["POST"])
def create():
    data = request.json
    response = create_quiz(data)
    return jsonify(response)

@quiz_bp.route("/questions/<int:quiz_id>", methods=["GET"])
def questions(quiz_id):
    questions = get_quiz_questions(quiz_id)
    return jsonify(questions)

@quiz_bp.route("/submit", methods=["POST"])
def submit():
    data = request.json
    response = submit_quiz_attempt(data)
    return jsonify(response)
