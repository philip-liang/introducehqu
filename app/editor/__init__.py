from flask import Blueprint


editor = Blueprint("editor", __name__)


from app.editor import forms, views
