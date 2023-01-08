from flaskeddit.models import AppUser

from flaskeddit import db



def get_user(username):
    """
    Gets a user by name from the database.
    """
    #Add your admin-username to make this user a Moderator
    #if username == 'adminusername':
    #    updateMod(username)
    user = AppUser.query.filter_by(username=username).first()
    email = user.email
    moderator = user.moderator
    return user, email, moderator


def updateMod(username):
    app_user = AppUser.query.filter_by(username=username.lower()).first()
    if app_user.moderator == False:
        app_user.moderator = True
        db.session.commit()
