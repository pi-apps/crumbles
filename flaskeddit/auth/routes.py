from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from flaskeddit.auth import auth_blueprint, auth_service
from flaskeddit.auth.forms import LoginForm, RegisterForm, ResetPasswordForm


@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    """
    Route for registering new users. On a GET request, it returns the registration
    form. On a POST request, it handles user registration.
    """
    if current_user.is_authenticated:
        return redirect(url_for("feed.feed"))
    form = RegisterForm()
    if form.validate_on_submit():
        auth_service.register_user(form.username.data, form.password.data, form.email.data)
        flash("Successfully registered.", "primary")
        return redirect(url_for("auth.login"))
    return render_template("register.html", form=form)


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    """
    Route for logging in users. On a GET request, it returns the login form. On a POST
    request, it handles user login.
    """
    if current_user.is_authenticated:
        return redirect(url_for("feed.feed"))
    form = LoginForm()
    if form.validate_on_submit():
        login_successful = auth_service.log_in_user(
            form.username.data, form.password.data
        )
        if login_successful:
            flash("Successfully logged in.", "primary")
            next_location = request.args.get("next")
            if next_location is None or not next_location.startswith("/"):
                next_location = url_for("feed.feed")
            return redirect(next_location)
        else:
            flash("Login Failed", "danger")
            return redirect(url_for("auth.login"))
    return render_template("login.html", form=form)

@auth_blueprint.route("/recoverpassword", methods=["GET", "POST"])
def recoverpassword():
    """
    Route for resetting a user password. On a GET request, it returns the recover form. On a POST
    request, it handles the password reset
    """
    form = ResetPasswordForm()
    if form.validate_on_submit():
        reset_successful = auth_service.reset_password(
            form.username.data, form.email.data
        )
        if reset_successful:
            flash("Successfully recovered password. Please check your email for more details", "primary")
            return redirect(url_for("auth.login"))
    return render_template("recoverpassword.html", form=form)

@auth_blueprint.route("/logout", methods=["POST"])
@login_required
def logout():
    """
    Route for logging out current users.
    """
    auth_service.log_out_user()
    flash("Successfully logged out.", "primary")
    return redirect(url_for("auth.login"))
