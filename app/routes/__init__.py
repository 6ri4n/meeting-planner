from .home import home_bp
from .event import event_bp

def init_app(app):
    app.register_blueprint(home_bp, url_prefix="/")
    app.register_blueprint(event_bp, url_prefix="/event")
