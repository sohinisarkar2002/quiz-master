from flask import Flask
from flask_migrate import Migrate
from backend.config import Config
from backend.database import db
from backend.models import *
from backend.routes.admin_routes import admin_bp
from backend.routes.quiz_routes import quiz_bp
from backend.routes.user_routes import user_bp
from backend.routes.auth_routes import auth_bp



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize database
    db.init_app(app)

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    # Create tables within the app context
    with app.app_context():
        db.create_all()

    # Register blueprints (modular routes)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(user_bp, url_prefix="/user")
    app.register_blueprint(quiz_bp, url_prefix="/quiz")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    # ✅ Add a simple home route
    @app.route("/")
    def home():
        return "Welcome to the Flask App!"

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
