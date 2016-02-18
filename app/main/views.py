from flask import render_template, request, current_app

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


@main.route("/passage_list", methods=["GET", "POST"])
def passage_list():
    page = request.args.get("page", 1, type=int)
    pagination = Passage.query.order_by(Passage.timestamp.desc()).paginate(page, per_page=current_app.config["INTROHQU_POSTS_PER_PAGE"], error_out=False)
    passages = pagination.items
    return render_template("main/passage_list.html", passages=passages, pagination=pagination)
