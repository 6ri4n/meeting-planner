from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON

db = SQLAlchemy()

class Event(db.Model):
    _id = db.Column(db.String(255), primary_key = True, autoincrement = False, nullable = False)
    event_name = db.Column(db.String(255), nullable = False)
    created_at = db.Column(db.String(255), nullable = False)
    start_time = db.Column(db.String(255), nullable = False) # UTC
    end_time = db.Column(db.String(255), nullable = False) # UTC
    participants = db.Column(JSON, nullable = False)
    available_days = db.Column(JSON, nullable = False)