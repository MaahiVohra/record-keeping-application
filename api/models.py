from flask_login import UserMixin
from __init__ import db


class User(UserMixin, db.Model):
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class Sample(db.Model):
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(10))
    nationality = db.Column(db.String(2))
    employment_type = db.Column(db.String(50))
    age = db.Column(db.Integer)
