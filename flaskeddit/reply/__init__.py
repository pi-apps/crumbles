from flask import Blueprint

reply_blueprint = Blueprint("reply", __name__)

from flaskeddit.reply import routes
