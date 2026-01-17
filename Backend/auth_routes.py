from flask import request, jsonify, session, redirect, url_for
from app import app, db
from models import User

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')

        # Check if the user exists
        user = User.query.filter_by(username=username, role=role).first()
        if not user or not user.check_password(password):
            return jsonify({"message": "Invalid credentials"}), 401

        # Set session data
        session['user_id'] = user.id
        session['username'] = user.username
        session['role'] = user.role
        session.modified = True  # Ensure session is saved
        print(f"User logged in: user_id={user.id}, username={user.username}, role={user.role}")  # Debug log

        # Redirect based on role
        if role == 'admin':
            return jsonify({"message": "Login successful", "redirect": "admin_dashboard.html"}), 200
        elif role == 'student':
            return jsonify({"message": "Login successful", "redirect": "home.html"}), 200
    except Exception as e:
        print(f"Error in /login: {e}")  # Debug log
        return jsonify({"message": "Internal server error"}), 500

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
