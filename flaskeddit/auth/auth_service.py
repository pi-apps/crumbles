from flask_login import login_user, logout_user
from passlib.hash import bcrypt

from flaskeddit import db
from flaskeddit.models import AppUser
from flaskeddit.config import Config


def register_user(username, password, email):
    """
    Hashes the given password and registers a new user in the database.
    """
    hashed_password = bcrypt.hash(password + Config.Server_SALT)
    email = email
    app_user = AppUser(username=username.lower(), password=hashed_password, email=email)
    db.session.add(app_user)
    db.session.commit()


def log_in_user(username, password):
    """
    Hashes and compares the given password with the stored password. If it is a match,
    logs a user in.
    """
    app_user = AppUser.query.filter_by(username=username.lower()).first()
    server_password = password + Config.Server_SALT
    if app_user and bcrypt.verify(server_password, app_user.password):
        login_user(app_user)
        return True
    else:
        return False


def log_out_user():
    """
    Logs the current user out.
    """
    logout_user()
