from flask import render_template

from flaskeddit.user import user_blueprint, user_service
from flask_login import current_user


@user_blueprint.route("/user/<string:username>")
def app_user(username):
    """
    Route displaying a user's profile page.
    """
    if current_user.is_authenticated:
        user, email, moderator = user_service.get_user(username)
        return render_template("user.html", app_user=user, access_name=current_user.username)
    else:
        user, email, moderator = user_service.get_user(username)
        return render_template("user.html", app_user=user)
