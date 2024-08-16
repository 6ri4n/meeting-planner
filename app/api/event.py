import base64
import json
import uuid
from datetime import date, datetime

from pytz import timezone as pytimezone, utc
from flask import Blueprint, jsonify, request

from ..models import Event, db

api_event_bp = Blueprint("api_event_bp", __name__)


@api_event_bp.route("/create", methods=["POST"])
def create_event():
    data = request.json
    if data:
        try:
            redirect_url = generate_base64_uuid()
            start_time_utc = convert_to_utc(data["startTimeSelector"], data["timezone"])
            end_time_utc = convert_to_utc(data["endTimeSelector"], data["timezone"])
            available_times = generate_utc_time_range(start_time_utc, end_time_utc)

            new_event = Event(
                _id=redirect_url,
                event_name=data["eventName"],
                created_at=date.today().strftime("%m-%d-%Y"),
                meeting={"days": data["selectedDays"], "times": available_times},
                participants={},
            )

            db.session.add(new_event)
            db.session.commit()

            return jsonify({"redirect_url": redirect_url})
        except Exception as err:
            return jsonify({"error": "Server Error. Please Try Again."}), 500
    else:
        return jsonify({"error": "Invalid Data."}), 400


@api_event_bp.route("/signin", methods=["POST"])
def signin():
    data = request.json
    if not data or not data.get("username") or not data.get("eventId"):
        return jsonify({"error": "Invalid Data."}), 400

    try:
        username = data["username"]
        event_id = data["eventId"]

        # Find the event by ID
        event = Event.query.get(event_id)
        if not event:
            return jsonify({"error": "Event not found."}), 404

        # Handles participants data
        if isinstance(event.participants, str):
            update_participants = json.loads(event.participants)
        else:
            update_participants = event.participants

        # Checks if the user already exists
        if username in update_participants:
            return (
                jsonify({"message": "User already exists."}),
                200,
            )  # 200 OK for idempotency

        # Add the new user
        update_participants[username] = {}
        event.participants = json.dumps(update_participants)
        db.session.commit()

        return jsonify({"username": username}), 201  # 201 Created for new user

    except Exception as err:
        print(f"Error: {err}")
        return jsonify({"error": "Server Error."}), 500  # 500 Internal Server Error


@api_event_bp.route("/update", methods=["POST"])
def update():
    data = request.json
    if (
        not data
        or not data.get("username")
        or not data.get("eventId")
        or not data.get("selectedTimes")
    ):
        return jsonify({"error": "Invalid Data."}), 400

    try:
        username = data["username"]
        event_id = data["eventId"]
        selected_times = data["selectedTimes"]

        # Finds the event by ID
        event = Event.query.get(event_id)
        if not event:
            return jsonify({"error": "Event not found."}), 404

        # Handles participants data
        if isinstance(event.participants, str):
            update_participants = json.loads(event.participants)
        else:
            update_participants = event.participants

        # Checks if the user is part of the event's participants
        if username not in update_participants:
            return jsonify({"error": "User not found in this event."}), 404

        # Update the user's data with the new selected times (overwrite old data)
        update_participants[username] = selected_times

        # Convert Dict to JSON string and commit
        event.participants = json.dumps(update_participants)
        db.session.commit()

        # Return 204 No Content if update was successful with no content to return
        return "", 204

    except Exception as err:
        print(f"Error: {err}")
        return jsonify({"error": "Server Error."}), 500  # 500 Internal Server Error


@api_event_bp.route("/users", methods=["POST"])
def users():
    data = request.json
    event_id = data.get("eventId")
    event = Event.query.get(event_id)
    # convert JSON string to Dict
    # users = json.loads(event.participants)
    # display list of usernames
    users = list(json.loads(event.participants).keys())
    return jsonify({"test": users}), 200


def generate_base64_uuid():
    u = uuid.uuid4()
    b64 = base64.urlsafe_b64encode(u.bytes[:8]).rstrip(b"=")
    return b64.decode("utf-8")


def convert_to_utc(time_str, timezone):
    # Parse the input time string to a naive datetime.time object
    naive_time = datetime.strptime(time_str, "%I:%M %p").time()

    # Combine with a date to create a naive datetime object
    naive_datetime = datetime.combine(datetime.today(), naive_time)

    # Get the timezone object for the given timezone
    tz = pytimezone(timezone)

    # Localize the naive datetime object with the given timezone
    localized_datetime = tz.localize(naive_datetime, is_dst=None)

    # Convert localized datetime to UTC
    utc_datetime = localized_datetime.astimezone(utc)

    # Format UTC datetime as string
    utc_time_str = utc_datetime.strftime("%H:%M")

    return utc_time_str


def generate_utc_time_range(start_time_utc, end_time_utc):
    start_hour = int(start_time_utc[:2])
    end_hour = int(end_time_utc[:2])
    available_times = []

    # Generate the time range
    if start_hour <= end_hour:
        for hour in range(start_hour, end_hour + 1):
            available_times.append(f"{hour:02d}:00")
    else:
        # Handle the wrap-around case
        for hour in range(start_hour, 24):
            available_times.append(f"{hour:02d}:00")
        for hour in range(0, end_hour + 1):
            available_times.append(f"{hour:02d}:00")

    return available_times
