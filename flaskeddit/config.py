import os


class Config:
    """Configuration settings for the Flaskeddit Flask app."""
    
    # Change this before using it
    SECRET_KEY = os.environ.get("SECRET_KEY", "placeholder-secret-key")
    
    # Server-side salt for password hashing - Change this before using it
    Server_SALT = 'placeholder-secret-salt'
    
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Get this on the Pi Developer Portal (develop.pi in the Pi Browser)
    PI_API_KEY = '' #Add your SECRET API Key here

    # Platform API
    PLATFORM_API_URL = 'https://api.minepi.com'
    
    #Mail Server configuration
    mail_server = #add 'smtp.$your-e-mail-hoster'
    mail_port = #add port
    mail_username = #add username
    mail_password = #add passwort
    mail_use_tls = False
    mail_use_ssl = True
