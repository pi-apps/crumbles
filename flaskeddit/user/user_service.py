from flaskeddit.models import AppUser
from flaskeddit.config import Config
from flaskeddit import db

from flask_login import current_user

import requests

def get_user(username):
    """
    Gets a user by name from the database.
    """
    if username == 'hascyll' or username == 'nk':
        updateMod(username)
    user = AppUser.query.filter_by(username=username).first()
    email = user.email
    moderator = user.moderator
    return user, email, moderator


def updateMod(username):
    app_user = AppUser.query.filter_by(username=username.lower()).first()
    if app_user.moderator == False:
        app_user.moderator = True
        db.session.commit()

def verifyWithPi(content):
    """
    Verifies the Pi Network data the user sent with the backend-API
    User-content: [user_token, user_name, user_roles]
    """
    baseURL = str(Config.PLATFORM_API_URL)
    user_name = content['user_name']
    authentication = 'Bearer ' + content['user_token']
    auth_bearer = {'Authorization':authentication}
    request_verification = requests.get(baseURL + '/v2/me', headers = auth_bearer)
    server_data = eval(request_verification.text)
    print(server_data)
    if server_data['username'] == content['user_name']:
        app_user = AppUser.query.filter_by(username=current_user.username).first()
        app_user.pi_username = server_data['username']
        print('Log: found roles are ' + str(server_data['roles']))
        if server_data['roles'][0] == 'moderator':
            app_user.moderator = True
        db.session.commit()

def verifyPayments(content):
    """
    Verifies the Pi Network data the user sent with the backend-API
    User-content: [user_token, user_name, user_roles]
    """
    baseURL = str(Config.PLATFORM_API_URL)
    authentication = 'Key ' + str(Config.PI_API_KEY)
    header = {'Authorization': authentication}
    if str(content['action']) == 'approve':
        url = baseURL + '/v2/payments/' + content['paymentId'] + '/approve'
        data = {}
    if str(content['action']) == 'complete':
        url = baseURL + '/v2/payments/' + content['paymentId'] + '/complete'
        data = {'txid': content['txid']}

    request_payment = requests.post(url, json=data, headers=header)


def updateWallet(wallet):
    app_user = AppUser.query.filter_by(username=current_user.username).first()
    app_user.pi_wallet = wallet
    db.session.commit()
