from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Events(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), nullable = False)
    password = db.Column(db.String(120), nullable = False)

    event_id = db.Column(db.Integer, nullable = False)
    event_creator = db.Column(db.Boolean, nullable = False)
    available_days = db.Column(db.String(255), nullable = False)  # Comma-separated string of dates
    time_range = db.Column(db.String(255), nullable = False)  # Comma-separated string of start and end times (UTC)