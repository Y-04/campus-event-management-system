from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from models import db  # Import db from models
from werkzeug.security import generate_password_hash
from models import User
import os

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)  # Initialize db with app
migrate = Migrate(app, db)

# Allow credentials and specify the frontend origin
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:8000"}}, supports_credentials=True)

# Serve static files from the Frontend directory
@app.route('/<path:filename>')
def serve_static_files(filename):
    try:
        return send_from_directory('../Frontend', filename)
    except Exception as e:
        print(f"Error serving static file {filename}: {e}")
        return "Static file not found", 404

# Serve images specifically from the Images folder
@app.route('/Images/<path:filename>')
def serve_images(filename):
    try:
        return send_from_directory('../Frontend/Images', filename)
    except Exception as e:
        print(f"Error serving image {filename}: {e}")
        return "Image not found", 404

@app.route('/static/posters/<path:filename>')
def serve_posters(filename):
    try:
        return send_from_directory(os.path.join(app.root_path, 'static/posters'), filename)
    except Exception as e:
        print(f"Error serving poster {filename}: {e}")
        return "Poster not found", 404

@app.route('/static/posters/default-poster.jpg')
def serve_default_poster():
    try:
        return send_from_directory('../Frontend/Images', 'default-poster.jpg')
    except Exception as e:
        print(f"Error serving default poster: {e}")
        return "Default poster not found", 404

# Ensure the static/posters directory exists
UPLOAD_FOLDER = os.path.join(app.root_path, 'static/posters')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

from routes import *

# Ensure tables are created and add default users
with app.app_context():
    db.create_all()

    # Add default admin and student users
    if not User.query.filter_by(username='admin').first():
        admin_user = User(username='admin', role='admin')
        admin_user.set_password('adminpass')  # Store plain text password
        db.session.add(admin_user)

    if not User.query.filter_by(username='student').first():
        student_user = User(username='student', role='student')
        student_user.set_password('studentpass')  # Store plain text password
        db.session.add(student_user)

    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True, port=8000)