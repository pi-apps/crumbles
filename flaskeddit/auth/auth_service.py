from flask_login import login_user, logout_user, current_user
from flask_mail import Mail, Message
from passlib.hash import bcrypt

from flaskeddit import db, mail
from flaskeddit.models import AppUser
from flaskeddit.config import Config

import secrets

def register_user(username, password, email):
    """
    Hashes the given password and registers a new user in the database.
    """
    hashed_password = bcrypt.hash(password + Config.Server_SALT)
    email = email
    app_user = AppUser(username=username.lower(), password=hashed_password, email=email)
    db.session.add(app_user)
    db.session.commit()

 def reset_password(username, email):
    """
    Generates a new password for a user and sends it to his/her email address.
    Note: There is no routine to check if the e-mail address is valid!
    """

    #find the user
    app_user = AppUser.query.filter_by(username=username.lower()).first()

    #If a user is found:
    if app_user:
        user_mail = app_user.email

        #generate a new random password
        password_length = 13
        new_password = secrets.token_urlsafe(password_length)

        #send the password
        recipient = []
        recipient.append(user_mail)
        recover_msg = Message('Reset crumbles password', sender = '$ADD-HERE-YOUR-EMAIL-ADDRESS', recipients = recipient)
        recover_msg.body = 'Dear user ' + str(username) + '\n\nThank you very much for testing this service!\n\nYour new password is: ' + str(new_password) + '\n\nNote: this is an automated email. Please do not respond.'

        mail.send(recover_msg)

        #updating the user-data after successful send
        app_user.password = bcrypt.hash(new_password + Config.Server_SALT) #here add salt!
        db.session.commit()
        return True
    else:
        return False

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

def changeEmail(email, password):
    """
    Lets a user change the used email-address.
    """
    username = current_user.username
    app_user = AppUser.query.filter_by(username=username.lower()).first()
    server_password = password + Config.Server_SALT
    if app_user and bcrypt.verify(server_password, app_user.password):
        app_user.email = email
        db.session.commit()
        return True
    else:
        return False

def changePassword(old_password, new_password):
    """
    Lets a user change the used email-address.
    """
    username = current_user.username
    app_user = AppUser.query.filter_by(username=username.lower()).first()
    old_server_password = old_password + Config.Server_SALT
    if app_user:
        if bcrypt.verify(old_server_password, app_user.password):
            app_user.password = bcrypt.hash(new_password + Config.Server_SALT)
            db.session.commit()
            return True
    else:
        return False

def log_out_user():
    """
    Logs the current user out.
    """
    logout_user()
