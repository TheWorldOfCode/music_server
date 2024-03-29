import os
from pathlib import Path

DOWNLOAD_DIR = "/tmp"


class BaseConfig:
    """ Base configuration """
    BASE_DIR = Path(__file__).parent
    TESTING = False

    MUSIC_DIR = os.environ.get("MUSIC_DIR", "/music")
    CORS_HEADERS = 'Content-Type'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", f"sqlite:///{BASE_DIR}/db.sqlite3")

    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0")
    CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/0")


class DevelopmentConfig(BaseConfig):
    """ Development configuration """
    DEBUG = True

class ProductionConfig(BaseConfig):
    """ Production configuration """
    DEBUG = False

config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}
