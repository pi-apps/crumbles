from flask import Blueprint

feed_blueprint = Blueprint("feed", __name__)

from flaskeddit.feed import routes
