from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    role = db.Column(db.String(50))


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(200))


class QuizQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    answer = db.Column(db.String(100))
    explanation = db.Column(db.Text)
    hint = db.Column(db.Text)
    topic = db.Column(db.String(100))


class QuizResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    topic = db.Column(db.String(100))
    is_correct = db.Column(db.Boolean)
    time_taken = db.Column(db.Integer)
    attempts = db.Column(db.Integer, default=1)
    hint_used = db.Column(db.Boolean, default=False)

