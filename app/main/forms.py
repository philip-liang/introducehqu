from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class CommentForm(Form):
    body = StringField("", validators=[Required()])
    submit = SubmitField("Submit")
