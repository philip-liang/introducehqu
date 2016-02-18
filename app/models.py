from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from flask.ext.login import UserMixin

from app import db
from app import login_manager


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.Unicode(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    admin_permission = db.Column(db.Boolean, default=False)
    passages = db.relationship("Passage", backref="author", lazy="dynamic")

    @property
    def password(self, password):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_administrator(self):
        return self.admin_permission

    def __repr__(self):
        return "<User %r>" % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Passage(db.Model):
    __tablename__ = "passages"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.UnicodeText)
    body = db.Column(db.UnicodeText)
    body_html = db.Column(db.UnicodeText)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __repr__(self):
        return "<Passage %r>" % self.id
