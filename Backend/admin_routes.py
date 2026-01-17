from flask import request, jsonify, session
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from app import app, db
from models import Event, Registration, User

UPLOAD_FOLDER = os.path.join(app.root_path, 'static/posters')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the upload folder exists

@app.route('/admin/add_event', methods=['POST'])
def add_event():
    # Ensure the user is logged in and has the 'admin' role
    if session.get('role') != 'admin':
        print("Unauthorized access attempt to add_event")  # Debug log
        return jsonify({"message": "Unauthorized"}), 403

    try:
        title = request.form.get('title')
        date = request.form.get('date')
        poster = request.files.get('poster')

        if not title or not date:
            return jsonify({"message": "Title and date are required"}), 400

        # Save the poster file if uploaded
        poster_path = None
        if poster:
            filename = secure_filename(poster.filename)
            poster_path = f"/static/posters/{filename}"
            poster.save(os.path.join(UPLOAD_FOLDER, filename))

        # Create a new event
        new_event = Event(title=title, date=date, poster_path=poster_path)
        db.session.add(new_event)
        db.session.commit()

        print(f"Event added successfully: {new_event.title}")
        return jsonify({"message": "Event added successfully"}), 201
    except Exception as e:
        print(f"Error in /admin/add_event: {e}")
        db.session.rollback()
        return jsonify({"message": "Internal server error"}), 500

@app.route('/admin/delete_event/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    # Ensure the user is logged in and has the 'admin' role
    if session.get('role') != 'admin':
        print("Unauthorized access attempt to delete_event")  # Debug log
        return jsonify({"message": "Unauthorized"}), 403

    event = Event.query.get(event_id)
    if event:
        try:
            # Delete associated registrations
            registrations = Registration.query.filter_by(event_id=event_id).all()
            for registration in registrations:
                db.session.delete(registration)

            # Commit the deletion of registrations before deleting the event
            db.session.commit()

            # Now delete the event
            db.session.delete(event)
            db.session.commit()
            return jsonify({"message": "Event and associated registrations deleted successfully"})
        except Exception as e:
            db.session.rollback()  # Rollback in case of an error
            return jsonify({"message": f"Failed to delete event: {e}"}), 500
    return jsonify({"message": "Event not found"}), 404

@app.route('/admin/clear_registrations', methods=['DELETE'])
def clear_registrations():
    if session.get('role') != 'admin':  # Validate admin role
        print("Unauthorized access attempt to clear_registrations")  # Debug log
        return jsonify({"message": "Unauthorized"}), 403

    try:
        # Delete all registrations
        registrations = Registration.query.all()
        print(f"Deleting {len(registrations)} registrations...")  # Debug log
        for registration in registrations:
            db.session.delete(registration)

        db.session.commit()
        return jsonify({"message": "All registrations cleared successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error clearing registrations: {e}")  # Debug log
        return jsonify({"message": "Failed to clear registrations"}), 500

@app.route('/admin/upload_poster/<int:event_id>', methods=['POST'])
def upload_poster(event_id):
    if 'username' not in session or session['role'] != 'admin':
        print("Unauthorized access attempt to upload_poster")  # Debug log
        return jsonify({"message": "Unauthorized"}), 403

    event = Event.query.get(event_id)
    if not event:
        return jsonify({"message": "Event not found"}), 404

    if 'poster' not in request.files:
        return jsonify({"message": "No file uploaded"}), 400

    file = request.files['poster']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    # Save the poster path in the database
    event.poster_path = f'/static/posters/{filename}'
    db.session.commit()
    return jsonify({"message": "Poster uploaded successfully", "poster_path": event.poster_path})

@app.route('/admin/edit_event/<int:event_id>', methods=['POST'])
def edit_event(event_id):
    # Ensure the user is logged in and has the 'admin' role
    if session.get('role') != 'admin':
        print("Unauthorized access attempt to edit_event")  # Debug log
        return jsonify({"message": "Unauthorized"}), 403

    try:
        title = request.form.get('title')
        date = request.form.get('date')
        poster = request.files.get('poster')

        if not title or not date:
            return jsonify({"message": "Title and date are required"}), 400

        event = Event.query.get(event_id)
        if not event:
            return jsonify({"message": "Event not found"}), 404

        # Update event details
        event.title = title
        event.date = date

        # Update poster if a new one is uploaded
        if poster:
            filename = secure_filename(poster.filename)
            poster_path = f"/static/posters/{filename}"
            poster.save(os.path.join(UPLOAD_FOLDER, filename))
            event.poster_path = poster_path

        db.session.commit()
        print(f"Event updated successfully: {event.title}")
        return jsonify({"message": "Event updated successfully"}), 200
    except Exception as e:
        print(f"Error in /admin/edit_event: {e}")
        db.session.rollback()
        return jsonify({"message": "Internal server error"}), 500

@app.route('/api/admin/stats', methods=['GET'])
def get_event_stats():
    try:
        events = Event.query.all()
        stats = []

        for event in events:
            registrations = Registration.query.filter_by(event_id=event.id).all()
            year_wise_count = {
                "1st Year": 0,
                "2nd Year": 0,
                "3rd Year": 0,
                "4th Year": 0
            }

            for registration in registrations:
                if registration.year_of_study in year_wise_count:
                    year_wise_count[registration.year_of_study] += 1

            stats.append({
                "event_title": event.title,
                "total_registrations": len(registrations),
                "year_wise": year_wise_count
            })

        return jsonify(stats), 200
    except Exception as e:
        print(f"Error fetching event stats: {e}")
        return jsonify({"message": "Internal server error"}), 500
