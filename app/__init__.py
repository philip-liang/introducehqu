from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from config import config


db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from app.editor import editor as editor_blueprint
    app.register_blueprint(editor_blueprint)

    return app


from app import models
