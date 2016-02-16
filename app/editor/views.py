from flask import render_template, redirect, url_for

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
        return redirect(url_for("main.show_passage"))

    return render_template("editor/edit_passage.html", form=form)
