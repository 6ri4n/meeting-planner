from flask import Blueprint, render_template
from ..models import Event
from pytz import common_timezones
import json

event_bp = Blueprint("event_bp", __name__)

@event_bp.route("/")
def event_home():
    return render_template("/event/index.html", title = "Event Home", message = "Event Home")

@event_bp.route("/create")
def create_event():
    return render_template("/event/create.html", title = "Create Event", message = "Create Event", timezones = common_timezones)

@event_bp.route("/<event_id>")
def event(event_id):
    event = Event.query.get(event_id)
    if event:
        return render_template("/event/event.html", availableDays = json.dumps(event.available_days), participants = event.participants)