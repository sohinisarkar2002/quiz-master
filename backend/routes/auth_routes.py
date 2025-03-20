from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from backend.database import db
from backend.models import User

auth_bp = Blueprint("auth", __name__)

# Registration
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "User already exists"}), 400

    hashed_pw = generate_password_hash(data["password"])
    new_user = User(username=data["username"], email=data["email"], password=hashed_pw, role="user")
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "User registered successfully"}), 201

# Login
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()

    if not user or not check_password_hash(user.password, data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    # Generate JWT token
    access_token = create_access_token(identity={"id": user.id, "role": user.role})
    return jsonify({"token": access_token, "user_id": user.id, "role": user.role}), 200


# Logout (Handled client-side by removing token)
@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    return jsonify({"message": "Logout successful"}), 200
