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
    return render_template(
        "/event/create.html",
        timezones = common_timezones,
        times = [
            "01:00 AM",
            "02:00 AM",
            "03:00 AM",
            "04:00 AM",
            "05:00 AM",
            "06:00 AM",
            "07:00 AM",
            "08:00 AM",
            "09:00 AM",
            "10:00 AM",
            "11:00 AM",
            "12:00 PM",
            "01:00 PM",
            "02:00 PM",
            "03:00 PM",
            "04:00 PM",
            "05:00 PM",
            "06:00 PM",
            "07:00 PM",
            "08:00 PM",
            "09:00 PM",
            "10:00 PM",
            "11:00 PM",
            "12:00 AM"
        ]
    )

@event_bp.route("/<event_id>")
def event(event_id):
    event = Event.query.get(event_id)
    if event:
        return render_template("/event/event.html", meeting = json.dumps(event.meeting), participants = event.participants)