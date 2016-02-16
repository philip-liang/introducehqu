from flask import render_template

from app.main import main
from app.models import Passage


@main.route("/")
@main.route("/index")
def index():
    return render_template("main/index.html")


@main.route("/show_passage")
def show_passage():
    passage = Passage.query.first()

    return render_template("main/show_passage.html", passage=passage)
