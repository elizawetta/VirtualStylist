from . import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    login = db.Column(db.String(1000))


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img_path = db.Column(db.String(100))
    clothes = db.Column(db.String(100))
    color_hsv = db.Column(db.Float)
    bl = db.Column(db.Float)
    wh = db.Column(db.Float)
    color = db.Column(db.String(100))


class Interaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    state = db.Column(db.Integer) # 1 - like, 2 - dislike, 0 - not viewed 
    date_time = db.Column(db.DateTime, nullable=True)




