from flask import render_template, request, current_app, flash, redirect, url_for
from flask.ext.login import current_user

from app import db
from app.main import main
from app.models import Passage, Comment
from app.main.forms import CommentForm


@main.route("/")
@main.route("/index")
def index():
    return render_template("main/index.html")


@main.route("/show_passage", methods=["GET", "POST"])
def show_passage():
    passage_id = request.args.get("id")
    passage = Passage.query.get_or_404(int(passage_id))
    form = CommentForm()

    if form.validate_on_submit():
        comment = Comment(
                      body=form.body.data,
                      passage=passage,
                      author=current_user._get_current_object()
                  )
        db.session.add(comment)
        flash("Your comment has been published.")
        return redirect(url_for("main.show_passage", id=passage.id))
    page = request.args.get("page", 1, type=int)
    pagination = passage.comments.order_by(Comment.timestamp.desc()).paginate(
                     page,
                     per_page=current_app.config["INTROHQU_COMMENTS_PER_PAGE"],
                     error_out=False
                 )
    comments = pagination.items

    return render_template(
               "main/show_passage.html",
                passage=passage,
                form=form,
                comments=comments,
                pagination=pagination
           )


@main.route("/passage_list", methods=["GET", "POST"])
def passage_list():
    page = request.args.get("page", 1, type=int)
    pagination = Passage.query.order_by(Passage.timestamp.desc()).paginate(page, per_page=current_app.config["INTROHQU_POSTS_PER_PAGE"], error_out=False)
    passages = pagination.items
    return render_template("main/passage_list.html", passages=passages, pagination=pagination)
