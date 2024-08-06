from .event import event_bp

def init_app(app):
    app.register_blueprint(event_bp, url_prefix="/")
