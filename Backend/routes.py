from app import app
from auth_routes import *
from event_routes import *
from admin_routes import *

@app.route('/')
def index():
    return "Backend is running. Use the frontend at http://127.0.0.1:8000/index.html"
