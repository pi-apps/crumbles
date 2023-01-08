import re

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError

from flaskeddit import db
from flaskeddit.models import Community


class CommunityForm(FlaskForm):
    """Form for creating a new community."""

    name = StringField("Name", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    submit = SubmitField("Create")

    def validate_name(self, name):
        """
        Validates that a given community name does not contain a space and is not taken
        by an existing community in the database.
        """
        #if re.search(" ", name.data):
        #    raise ValidationError("Name cannot contain a space.")

        community = Community.query.filter(
            db.func.lower(Community.name) == name.data.lower()
        ).first()
        if community is not None:
            raise ValidationError("Name is already taken.")


class UpdateCommunityForm(FlaskForm):
    """Form for updating a community description."""

    description = TextAreaField("Description", validators=[DataRequired()])
    submit = SubmitField("Update")
