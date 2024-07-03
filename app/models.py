from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Event(db.Model):
    _id = db.Column(db.Integer, primary_key = True, autoincrement = False, nullable = False)
    event_name = db.Column(db.String(255), nullable = False)
    created_at = db.Column(db.String(255), nullable = False)
    available_days = db.Column(db.String(255), nullable = False) # Comma-separated string of dates
    time_range = db.Column(db.String(255), nullable = False) # Comma-separated string of start and end times (UTC)

    users = db.relationship('User', backref = 'event', lazy = True)


class User(db.Model):
    _id = db.Column(db.Integer, primary_key = True)
    event_id = db.Column(db.Integer, db.ForeignKey('event._id'), nullable = False)
    username = db.Column(db.String(80), nullable = False)
    password = db.Column(db.String(120), nullable = False)
    available_days = db.Column(db.String(255), default = None) # Comma-separated string of dates
    available_time = db.Column(db.String(255), default = None) # Comma-separated string of start and end times (UTC)