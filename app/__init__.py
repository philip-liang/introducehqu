from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.moment import Moment
from flask.ext.login import LoginManager
from flask.ext.mail import Mail

from config import config


db = SQLAlchemy()
moment = Moment()
mail = Mail()
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from app.editor import editor as editor_blueprint
    app.register_blueprint(editor_blueprint)
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app


from app import models, email
