from flask import Blueprint

event_views = Blueprint("event_views", __name__)


@event_views.route('/')
def event_home():
    return '<h1>Event Home</h1>'