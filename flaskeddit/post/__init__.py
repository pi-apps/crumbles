from flask import Blueprint

post_blueprint = Blueprint("post", __name__)

from flaskeddit.post import routes
