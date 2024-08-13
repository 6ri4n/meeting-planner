from flask import Flask
from flask_cors import CORS


def create_app():
    from .config import Config
    from .models import db

    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    from . import api, routes

    routes.init_app(app)
    api.init_app(app)

    return app
