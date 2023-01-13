from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length

from flaskeddit.models import AppUser

CT_usernames = ['nk', 'nicolas', 'cfan', 'aurelienshz', 'swaroop', 'cryptoging', 'philosopherchris', 'h3rcy', 'kbiyo1', 'sherriorange', 'agares18', 'dunkinboy', 'edwaardkang', 'gamebuyer', 'greglalumiere', 'hugoa', 'ihatejam', 'jonziv', 'lyriaaw', 'oaklee', 'swetate', 'warnz99', 'zzzchen']

class RegisterForm(FlaskForm):
    """Form for registering a new user."""

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            EqualTo("confirm_password", message="Passwords must match."),
            Length(min=6),
        ],
    )
    email = StringField("Email", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_username(self, username):
        """
        Validates that a user with the given username does not already exist in the
        database.
        """
        app_user = AppUser.query.filter_by(username=username.data.lower()).first()
        if app_user is not None:
            if str(app_user.username) in CT_usernames:
                raise ValidationError("Restricted Username.")
            else:
                raise ValidationError("Username is taken.")


class LoginForm(FlaskForm):
    """Form for logging in a user."""
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")

class ChangeEmailForm(FlaskForm):
    """Form for changing the email of a user."""

    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Confirm new Email")

class ChangePasswordForm(FlaskForm):
    """Form for logging in a user."""
    old_password = PasswordField("Old Password", validators=[DataRequired()])
    new_password = PasswordField(
        "New Password",
        validators=[
            DataRequired(),
            EqualTo("confirm_newpassword", message="Passwords must match."),
            Length(min=6),
        ],
    )
    confirm_newpassword = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Confirm new Password")
    
class ResetPasswordForm(FlaskForm):
    """Form for resetting a password."""
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("E-Mail", validators=[DataRequired()])
    submit = SubmitField("Reset Password")

