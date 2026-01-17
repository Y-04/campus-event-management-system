from flask import request, jsonify, session
from app import app, db
from models import Registration

@app.route('/student/clear_history', methods=['DELETE'])
def clear_history():
    if session.get('role') != 'student':  # Validate student role
        return jsonify({"message": "Unauthorized"}), 403

    user_id = session.get('user_id')
    try:
        # Delete all registrations for the logged-in student
        registrations = Registration.query.filter_by(user_id=user_id).all()
        if registrations:
            print(f"Clearing {len(registrations)} registrations for user ID: {user_id}")  # Debug log
        for registration in registrations:
            db.session.delete(registration)

        db.session.commit()
        return jsonify({"message": "Event history cleared successfully"})
    except Exception as e:
        print(f"Error clearing event history: {e}")  # Debug log
        db.session.rollback()
        return jsonify({"message": "Failed to clear event history"}), 500
