from backend.models import User

def get_all_users():
    users = User.query.all()
    return [{"id": u.id, "username": u.username, "email": u.email, "role": u.role} for u in users]
