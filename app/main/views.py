from flask import render_template, request

from app.main import main
from app.models import Passage


@main.route("/")
@main.route("/index")
def index():
    return render_template("main/index.html")


@main.route("/show_passage")
def show_passage():
    passage_id = request.args.get("id")
    passage = Passage.query.get_or_404(int(passage_id))

    return render_template("main/show_passage.html", passage=passage)


@main.route("/passage_list")
def passage_list():
    passages = Passage.query.order_by(Passage.timestamp.desc()).all()
    return render_template("main/passage_list.html", passages=passages)
