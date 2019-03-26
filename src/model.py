from datetime import datetime

from . import db


class VideoPair(db.Model):
    file_ID = db.Column(db.String(80), primary_key=True, unique=True, nullable=False)
    method_A = db.Column(db.String(80), nullable=False)
    method_B = db.Column(db.String(80), nullable=False)
    mask_type = db.Column(db.String(80), nullable=False)
    mask_ratio = db.Column(db.String(80), nullable=False)
    answer_A = db.Column(db.Integer, nullable=False, default=0)
    answer_B = db.Column(db.Integer, nullable=False, default=0)


class SurveyData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    video_pairs = db.Column(db.String(8000), nullable=False)


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    file_ID = db.Column(db.String(80), nullable=False)
    ans = db.Column(db.String(80), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80),  unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now)


db.create_all()
