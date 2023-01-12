from flask import render_template, request

from flaskeddit.user import user_blueprint, user_service

from flask_login import current_user


@user_blueprint.route("/user/<string:username>", methods=['GET','POST'])
def app_user(username):
    """
    Route displaying a user's profile page.
    """
    if request.method == 'POST':
        try:
            try:
                content = request.json
                try:
                    if content['user_name']:
                        print('Log: received data for user ' + str(current_user.username) + ', Pi Network Username: ' + str(content['user_name']))
                        user_service.verifyWithPi(content)
                except:
                    pass
                try:
                    if str(content['action']) == 'approve' or str(content['action']) == 'complete':
                        user_service.verifyPayments(content)
                except:
                    pass
            except:
                pass
            try:
                content = request.form['wallet']
                if len(content) == 56 and content[0] == 'G':
                    user_service.updateWallet(content)
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
