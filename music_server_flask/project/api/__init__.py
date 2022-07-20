from flask_cors import CORS

from .library import library_blueprint
from .youtube import youtube_blueprint
from .download_manager import download_manager

def register_api(app):
    """ Register the blueprints """
    CORS(app, resources={r"/api": {"origins": "*"}})

    app.register_blueprint(library_blueprint)
    app.register_blueprint(youtube_blueprint)
    app.register_blueprint(download_manager)