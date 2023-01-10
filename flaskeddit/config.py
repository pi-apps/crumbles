import os


class Config:
    """Configuration settings for the Flaskeddit Flask app."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "placeholder-secret-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Get this on the Pi Developer Portal (develop.pi in the Pi Browser)
    PI_API_KEY = '' #Add your API Key here

    # Platform API
    PLATFORM_API_URL = 'https://api.minepi.com'
