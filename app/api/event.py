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
        redirect_url = generate_base64_uuid()
        start_time_utc = convert_to_utc(data["startTimeSelector"], data["timezone"])
        end_time_utc = convert_to_utc(data["endTimeSelector"], data["timezone"])
        available_times = generate_time_range(start_time_utc, end_time_utc)

        for days in data["availableDays"]:
            days["availableTimes"] = available_times

        new_event = Event(
            _id = redirect_url, 
            event_name = data["eventName"], 
            created_at = date.today().strftime("%m-%d-%Y"), 
            start_time = start_time_utc, 
            end_time = end_time_utc, 
            available_days = data["availableDays"],
            participants = data["participants"]
        )

        db.session.add(new_event)
        db.session.commit()
        return jsonify({"redirect_url": redirect_url})
    else:
        return jsonify({"error": "Invalid Data."}), 400
    
def generate_base64_uuid():
    u = uuid.uuid4()
    b64 = base64.urlsafe_b64encode(u.bytes).rstrip(b'=')
    return b64.decode('utf-8')

def convert_to_utc(time_str, timezone):
    # Parse the input time string to a naive datetime.time object
    naive_time = datetime.strptime(time_str, '%I:%M%p').time()
    
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

def generate_time_range(start_time_utc, end_time_utc):
    # Parse the input times
    start_hour = int(start_time_utc[:2])
    end_hour = int(end_time_utc[:2])
    available_times = []

    # Define a helper to format the time key
    def format_time_key(hour):
        return f"{hour:02d}:00"

    # Generate the time range
    if start_hour <= end_hour:
        for hour in range(start_hour, end_hour + 1):
            time_key = format_time_key(hour)
            available_times.append({time_key: {"available": [], "unavailable": []}})
    else:
        # Handle the wrap-around case
        for hour in range(start_hour, 24):
            time_key = format_time_key(hour)
            available_times.append({time_key: {"available": [], "unavailable": []}})
        for hour in range(0, end_hour + 1):
            time_key = format_time_key(hour)
            available_times.append({time_key: {"available": [], "unavailable": []}})

    return available_times