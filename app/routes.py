from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    title = "Meeting Planner"
    message = "This is meeting-planner"
    return render_template('index.html', title=title, message=message)