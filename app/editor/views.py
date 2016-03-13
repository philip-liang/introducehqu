from flask import render_template, redirect, url_for, request, flash
from flask.ext.login import current_user, login_required

from app import db
from app.models import Passage, PassageType
from app.summary import SummaryText
from app.editor import editor
from app.editor.forms import EditorForm


@editor.route("/edit_passage", methods=["GET", "POST"])
@login_required
def edit_passage():
    form = EditorForm()
    form.passage_type.choices = [(t.id, t.name) for t in PassageType.query.order_by("name")]

    if form.validate_on_submit():
        summary = SummaryText(form.body.data)
        passage = Passage(
            title = form.title.data,
            body = summary.get_summary(),
            body_html=form.body.data,
            passage_type=form.passage_type.data,
            author=current_user._get_current_object()
        )
        db.session.add(passage)
        db.session.commit()
        return redirect(url_for("main.show_passage", id=passage.id))

    return render_template("editor/edit_passage.html", form=form)


@editor.route("/review_passage", methods=["GET", "POST"])
@login_required
def review_passage():
    form = EditorForm()
    passage_id = request.args.get("id")
    passage = Passage.query.get(int(passage_id))

    if current_user.id != passage.author.id and \
            not current_user.is_administrator():
        flash("You have no permission.")
        return redirect(url_for("main.show_passage", id=int(passage_id)))

    if form.validate_on_submit():
        summary = SummaryText(form.body.data)
        passage.title = form.title.data
        passage.body = summary.get_summary()
        passage.body_html = form.body.data
        db.session.add(passage)
        return redirect(url_for("main.show_passage", id=int(passage_id)))
    elif passage is not None:
        form.title.data = passage.title
        form.body.data = passage.body_html

    return render_template("editor/edit_passage.html", form=form)


@editor.route("/delete_passage")
@login_required
def delete_passage():
    passage_id = request.args.get("id")
    passage = Passage.query.get(int(passage_id))

    if current_user.id != passage.author.id and \
            not current_user.is_administrator():
        flash("You have no permission.")
        return redirect(url_for("main.show_passage", id=int(passage_id)))

    if passage is not None:
        db.session.delete(passage)
    return redirect(url_for("main.index"))
