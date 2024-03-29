import os

from flask import Flask
from flask_celeryext import FlaskCeleryExt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from project.celery_utils import make_celery
from project.config import config
from project.manager import Manager as TaskManager


# Instantiate the extensions
db = SQLAlchemy()
migrate = Migrate()
ext_celery = FlaskCeleryExt(create_celery_app=make_celery)
task_manager = TaskManager()


def create_app(config_name=None):
    """ Create the app """

    if config_name is None:
        config_name = os.environ.get("FLASK_CONFIG", "development")

    app = Flask(__name__)

    CORS(app)

    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    ext_celery.init_app(app)
    task_manager.init_app(ext_celery.celery)

    from project.api import register_api
    register_api(app)

    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}
    
    return app
    