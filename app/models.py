# app/models.py
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    poster_url = db.Column(db.Text)
    video_url = db.Column(db.Text)
    created_at = db.Column(db.DateTime)