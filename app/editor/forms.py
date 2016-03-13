from flask.ext.wtf import Form
from wtforms import TextAreaField, SubmitField, SelectField
from wtforms.validators import Required


class EditorForm(Form):
    title = TextAreaField("title", validators=[Required()])
    passage_type = SelectField("Type", coerce=int)
    body = TextAreaField("Hello!", validators=[Required()])
    submit = SubmitField("Submit")
