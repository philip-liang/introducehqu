from flask import render_template, redirect, url_for, request

from app import db
from app.models import Passage
from app.editor import editor
from app.editor.forms import EditorForm


@editor.route("/edit_passage", methods=["GET", "POST"])
def edit_passage():
    form = EditorForm()

    if form.validate_on_submit():
        passage = Passage(body_html=form.body.data)
        db.session.add(passage)
        return redirect(url_for("main.show_passage", id=passage.id))

    return render_template("editor/edit_passage.html", form=form)


@editor.route("/review_passage", methods=["GET", "POST"])
def review_passage():
    form = EditorForm()
    passage_id = request.args.get("id")
    passage = Passage.query.get(int(passage_id))

    if form.validate_on_submit():
        passage.body_html = form.body.data
        db.session.add(passage)
        return redirect(url_for("main.show_passage", id=int(passage_id)))
    elif passage is not None:
        form.body.data = passage.body_html

    return render_template("editor/edit_passage.html", form=form)


@editor.route("/delete_passage")
def delete_passage():
    passage_id = request.args.get("id")
    passage = Passage.query.get(int(passage_id))
    if passage is not None:
        db.session.delete(passage)
    return redirect(url_for("main.index"))
