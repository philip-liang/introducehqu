from datetime import datetime

from app import db


class Passage(db.Model):
    __tablename__ = "passages"

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.UnicodeText)
    body_html = db.Column(db.UnicodeText)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
