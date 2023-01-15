from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField

class ReplyForm(FlaskForm):
    """Form for creating and updating a reply."""

    reply = CKEditorField("Reply", validators=[DataRequired()])
    submit = SubmitField("Submit")
