from flask import Flask
from .models import db
from .config import Config

app = Flask(__name__)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    
    with app.app_context():
        db.create_all()

    from .views.views import views
    from .views.event_views import event_views
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(event_views, url_prefix='/event')

    return app