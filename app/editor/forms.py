from flask.ext.wtf import Form
from wtforms import TextAreaField, SubmitField
from wtforms.validators import Required


class EditorForm(Form):
    title = TextAreaField("title", validators=[Required()])
    body = TextAreaField("Hello!", validators=[Required()])
    submit = SubmitField("Submit")
