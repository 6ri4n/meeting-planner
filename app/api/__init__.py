from .event import api_event_bp


def init_app(app):
    app.register_blueprint(api_event_bp, url_prefix="/api/event")
