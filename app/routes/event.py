from flask import Blueprint, render_template
from ..models import Event, User
import pytz

event_bp = Blueprint("event_bp", __name__)

@event_bp.route("/")
def event_home():
    return render_template("/event/index.html", title = "Event Home", message = "Event Home")

@event_bp.route("/create")
def create_event():
    return render_template("/event/create.html", title = "Create Event", message = "Create Event", timezones = pytz.common_timezones)

@event_bp.route("/<event_id>/members")
def event_members(event_id):
    event = Event.query.get(event_id)
    if event:
        return render_template("/event/members.html", title = "View Event", message = f"Event: {event_id}", participants = event.users)

@event_bp.route("/<event_id>")
def event(event_id):
    pass