from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_ckeditor import CKEditor

from flaskeddit.config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "danger"
mail = Mail()
ckeditor = CKEditor()

def create_app(config=Config):
    """
    Factory method for creating the Flaskeddit Flask app.
    https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/
    """
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    login_manager.init_app(app)
    
    app.config['MAIL_SERVER']= Config.mail_server
    app.config['MAIL_PORT'] = Config.mail_port
    app.config['MAIL_USERNAME'] = Config.mail_username
    app.config['MAIL_PASSWORD'] = Config.mail_password
    app.config['MAIL_USE_TLS'] = Config.mail_use_tls
    app.config['MAIL_USE_SSL'] = Config.mail_use_ssl
    mail = Mail(app)
    
    ckeditor.init_app(app)

    from flaskeddit.auth import auth_blueprint
    from flaskeddit.communities import communities_blueprint
    from flaskeddit.community import community_blueprint
    from flaskeddit.feed import feed_blueprint
    from flaskeddit.post import post_blueprint
    from flaskeddit.reply import reply_blueprint
    from flaskeddit.user import user_blueprint
    from flaskeddit.cli import cli_app_group

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(communities_blueprint)
    app.register_blueprint(community_blueprint)
    app.register_blueprint(feed_blueprint)
    app.register_blueprint(post_blueprint)
    app.register_blueprint(reply_blueprint)
    app.register_blueprint(user_blueprint)
    app.cli.add_command(cli_app_group)

    return app
