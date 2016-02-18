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

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u = User(
                email=forgery_py.internet.email_address(),
                username=forgery_py.internet.user_name(True),
                password=forgery_py.lorem_ipsum.word(),
                admin_permission=False
            )
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()


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

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py

        seed()
        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count - 1)).first()
            p = Passage(
                title=forgery_py.internet.user_name(True),
                body=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                timestamp=forgery_py.date.date(True),
                author=u
            )
            db.session.add(p)
            db.session.commit()
