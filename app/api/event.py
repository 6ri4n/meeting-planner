from flask import Blueprint, request, jsonify
import uuid
import base64
from datetime import datetime, date
import pytz
from ..models import Event, db

api_event_bp = Blueprint("api_event_bp", __name__)

@api_event_bp.route("/create", methods = ["POST"])
def create_event():
    data = request.json
    if data:
        try:
            redirect_url = generate_base64_uuid()
            start_time_utc = convert_to_utc(data["startTimeSelector"], data["timezone"])
            end_time_utc = convert_to_utc(data["endTimeSelector"], data["timezone"])
            available_times = generate_utc_time_range(start_time_utc, end_time_utc)

            new_event = Event(
                _id = redirect_url, 
                event_name = data["eventName"], 
                created_at = date.today().strftime("%m-%d-%Y"),
                meeting = {"days": data["selectedDays"], "times": available_times},
                participants = {}
            )

            db.session.add(new_event)
            db.session.commit()

            return jsonify({"redirect_url": redirect_url})
        except Exception as err:
            return jsonify({"error": "Server Error. Please Try Again."}), 500
    else:
        return jsonify({"error": "Invalid Data."}), 400
    
def generate_base64_uuid():
    u = uuid.uuid4()
    b64 = base64.urlsafe_b64encode(u.bytes[:8]).rstrip(b'=')
    return b64.decode('utf-8')

def convert_to_utc(time_str, timezone):
    # Parse the input time string to a naive datetime.time object
    naive_time = datetime.strptime(time_str, '%I:%M %p').time()
    
    # Combine with a date to create a naive datetime object
    naive_datetime = datetime.combine(datetime.today(), naive_time)
    
    # Get the timezone object for the given timezone
    tz = pytz.timezone(timezone)
    
    # Localize the naive datetime object with the given timezone
    localized_datetime = tz.localize(naive_datetime, is_dst=None)
    
    # Convert localized datetime to UTC
    utc_datetime = localized_datetime.astimezone(pytz.utc)
    
    # Format UTC datetime as string
    utc_time_str = utc_datetime.strftime('%H:%M')
    
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