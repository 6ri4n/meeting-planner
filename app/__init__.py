from flask import Flask
from flask_cors import CORS

def create_app():
    from .models import db
    from .config import Config
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)
    db.init_app(app)
    
    with app.app_context():
        db.create_all()

    from . import routes, api
    routes.init_app(app)
    api.init_app(app)


    return app