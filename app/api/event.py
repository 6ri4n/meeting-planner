from flask import Blueprint, redirect, url_for, render_template, request, jsonify

api_event_bp = Blueprint("api_event_bp", __name__)

@api_event_bp.route("/create", methods = ["POST"])
def create_event():
    data = request.json
    if data and "eventName" in data:
        eventName = data["eventName"]
        return redirect(url_for("api_event_bp.test_event", eventName = eventName))
    else:
        return jsonify({"error": "Event Name not provided"}), 400

@api_event_bp.route("/test/<eventName>")
def test_event(eventName):
    return render_template("/event/test.html", eventName = eventName)