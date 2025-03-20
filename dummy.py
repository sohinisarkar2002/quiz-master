from backend.database import db
from flask import Flask
from sqlalchemy import inspect

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db.init_app(app)

with app.app_context():
    inspector = inspect(db.engine)
    print(inspector.get_table_names())
