from flask import render_template, request

from flaskeddit.user import user_blueprint, user_service
from flaskeddit.models import AppUser
from flaskeddit.config import Config
from flask_login import current_user
from flaskeddit import db

import requests

@user_blueprint.route("/user/<string:username>", methods=['GET','POST'])
def app_user(username):
    """
    Route displaying a user's profile page.
    """
    if request.method == 'POST':
        try:
            try:	
                content = request.json
                print(content)
                print(type(content))
                print(content['action'])
                try:
                    if content['user_name']:
                        print('Log: received data for user ' + str(current_user.username) + ', Pi Network Username: ' + str(content['user_name']))
                        verifyWithPi(content)
                except: 
                    pass
                try:
                    if str(content['action']) == 'approve' or str(content['action']) == 'complete':
                        verifyPayments(content)
                except: 
                    pass
            except:
                pass
            try:
                content = request.form['wallet']
                if len(content) == 56 and content[0] == 'G':
                    updateWallet(content)	
            except:
                pass
        except:
    	    print('Error during VerifyWithPi-Routine')
    if current_user.is_authenticated:
        user, email, moderator = user_service.get_user(username)
        return render_template("user.html", app_user=user, access_name=current_user.username)
    else:
        user, email, moderator = user_service.get_user(username)
        return render_template("user.html", app_user=user)

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
