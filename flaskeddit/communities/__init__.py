from flask import Blueprint

communities_blueprint = Blueprint("communities", __name__)

from flaskeddit.communities import routes
