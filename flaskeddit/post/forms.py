from flask_wtf import FlaskForm
from wtforms.fields import IntegerField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError

from flaskeddit.models import Post


class PostForm(FlaskForm):
    """Form for creating a new post."""

    title = StringField("Title", validators=[DataRequired()])
    post = TextAreaField("Post", validators=[DataRequired()])
    community_id = IntegerField("Community Id", validators=[DataRequired()])
    submit = SubmitField("Create")

    def validate_title(self, title):
        """
        Validates that a given title is not already taken by an existing post within
        the target community in the database.
        """
        post = Post.query.filter_by(
            title=title.data, community_id=self.community_id.data
        ).first()
        if post is not None:
            raise ValidationError(
                "Post with same title already exists within this community."
            )


class UpdatePostForm(FlaskForm):
    """Form for updating a post."""

    post = TextAreaField("Post", validators=[DataRequired()])
    submit = SubmitField("Create")
