from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Store hashed passwords
    role = db.Column(db.String(10), nullable=False)  # "admin" or "student"

    def set_password(self, password):
        self.password = generate_password_hash(password)  # Hash the password

    def check_password(self, password):
        return check_password_hash(self.password, password)  # Verify the password

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    tagline = db.Column(db.String(255), default="Join us for an unforgettable experience!")  # New column
    poster_path = db.Column(db.String(255), nullable=True)  # New column

class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    year_of_study = db.Column(db.String(20), nullable=True)  # Added year_of_study to store the student's year during registration
