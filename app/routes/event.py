import json

from flask import Blueprint, render_template

from ..config import common_timezones, time_format
from ..models import Event

event_bp = Blueprint("event_bp", __name__)


@event_bp.route("/")
def event_home():
    return render_template(
        "/event/index.html", title="Event Home", message="Event Home"
    )


@event_bp.route("/plan")
def create_event():
    return render_template(
        "/event/create.html", timezones=common_timezones, times=time_format
    )


@event_bp.route("/<event_id>")
def event(event_id):
    event = Event.query.get(event_id)
    if event:
        return render_template(
            "/event/event.html",
            meeting=json.dumps(event.meeting),
            participants=event.participants,
            description=event.description,
            event_name=event.event_name,
            timezones=common_timezones
        )
