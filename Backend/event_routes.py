from flask import request, jsonify, session
from app import app, db
from models import Event, Registration, User
from datetime import datetime

def parse_event_date(date_str):
    """Try multiple date formats for event.date."""
    for fmt in ("%Y-%m-%d", "%d-%m-%Y %H:%M:%S"):
        try:
            return datetime.strptime(date_str, fmt).date()
        except Exception:
            continue
    raise ValueError(f"Unknown date format: {date_str}")

@app.route('/events', methods=['GET'])
def get_events():
    try:
        events = Event.query.all()
        current_date = datetime.now().date()

        upcoming_events = []
        past_events = []

        for event in events:
            # Ensure event.date is a valid datetime object
            try:
                if isinstance(event.date, str):
                    event_date = parse_event_date(event.date)
                else:
                    event_date = event.date
            except Exception as e:
                print(f"Invalid date format for event ID {event.id}: {event.date}. Error: {e}")
                continue

            # Handle NULL poster paths
            poster_path = event.poster_path or "/static/posters/default-poster.jpg"

            event_data = {
                "id": event.id,
                "title": event.title,
                "date": event_date.strftime("%Y-%m-%d"),
                "tagline": event.tagline,
                "poster_path": f"http://127.0.0.1:5000{poster_path}"
            }

            # Always include all events, split by date
            if event_date >= current_date:
                upcoming_events.append(event_data)
            else:
                past_events.append(event_data)

        print(f"Events fetched successfully. Upcoming: {len(upcoming_events)}, Past: {len(past_events)}")  # Debug log
        return jsonify({"upcoming": upcoming_events, "past": past_events}), 200
    except Exception as e:
        print(f"Error fetching events: {e}")
        return jsonify({"message": "Internal server error"}), 500

@app.route('/register_event', methods=['POST'])
def register_event():
    try:
        data = request.json
        event_id = data.get('event_id')
        year = data.get('year')
        user_id = session.get('user_id')  # Get user_id from session

        print(f"Received data: event_id={event_id}, year={year}, user_id={user_id}")

        if not event_id or not year or not user_id:
            print("Invalid data: Missing event_id, year, or user_id")
            return jsonify({"message": "Invalid data"}), 400

        event = Event.query.filter_by(id=event_id).first()
        if not event:
            print(f"Event not found: event_id={event_id}")
            return jsonify({"message": "Event not found"}), 404

        # Ensure event.date is a valid datetime object
        if isinstance(event.date, str):
            event_date = parse_event_date(event.date)
        else:
            event_date = event.date

        existing_registration = Registration.query.filter_by(user_id=user_id, event_id=event_id).first()
        if existing_registration:
            print(f"Registration already exists for user_id={user_id}, event_id={event_id}")
            return jsonify({"message": "You are already registered for this event"}), 400

        current_date = datetime.now().date()
        if event_date < current_date:
            print(f"Cannot register for outdated event: event_id={event_id}, event_date={event_date}")
            return jsonify({"message": "Cannot register for an outdated event"}), 400

        registration = Registration(user_id=user_id, event_id=event_id, year_of_study=year)
        db.session.add(registration)
        db.session.commit()
        print(f"Registration successful for user_id={user_id}, event_id={event_id}, year={year}")
        return jsonify({"message": "Event registered successfully"}), 201
    except Exception as e:
        print(f"Error in /register_event: {e}")
        db.session.rollback()
        return jsonify({"message": "Internal server error"}), 500

@app.route('/student_events/<username>', methods=['GET'])
def student_events(username):
    try:
        print(f"Fetching registered events for username: {username}")
        if not username or username == "null":
            print("Invalid username provided")
            return jsonify({"message": "Invalid username"}), 400

        user = User.query.filter_by(username=username).first()
        if not user:
            print(f"User not found: {username}")
            return jsonify({"message": "User not found"}), 404

        registrations = Registration.query.filter_by(user_id=user.id).all()
        if not registrations:
            print(f"No registered events found for user: {username}")
            return jsonify({"upcoming": [], "past": []}), 200

        upcoming_events = []
        past_events = []
        current_date = datetime.now().date()
        seen_event_ids = set()

        for r in registrations:
            event = Event.query.get(r.event_id)
            if event and event.id not in seen_event_ids:
                seen_event_ids.add(event.id)
                try:
                    if isinstance(event.date, str):
                        event_date = parse_event_date(event.date)
                    else:
                        event_date = event.date
                except Exception as e:
                    print(f"Invalid date format for event ID {event.id}: {event.date}. Error: {e}")
                    continue

                poster_path = event.poster_path or "/static/posters/default-poster.jpg"
                event_data = {
                    "id": event.id,
                    "title": event.title,
                    "date": event_date.strftime("%Y-%m-%d"),
                    "poster_path": f"http://127.0.0.1:5000{poster_path}"
                }
                if event_date >= current_date:
                    upcoming_events.append(event_data)
                else:
                    past_events.append(event_data)

        print(f"Upcoming events: {upcoming_events}, Past events: {past_events}")
        return jsonify({"upcoming": upcoming_events, "past": past_events})
    except Exception as e:
        print(f"Error in /student_events/{username}: {e}")
        return jsonify({"message": "Internal server error"}), 500

@app.route('/events/calendar', methods=['GET'])
def get_calendar_events():
    try:
        events = Event.query.all()
        calendar_events = []

        for event in events:
            try:
                if isinstance(event.date, str):
                    event_date = parse_event_date(event.date)
                else:
                    event_date = event.date
            except Exception as e:
                print(f"Invalid date format for event ID {event.id}: {event.date}. Error: {e}")
                continue

            calendar_events.append({
                "id": event.id,
                "title": event.title,
                "start": event_date.strftime("%Y-%m-%d"),
                "tagline": event.tagline,
                "poster_path": event.poster_path
            })

        print("Calendar events fetched successfully.")
        return jsonify(calendar_events), 200
    except Exception as e:
        print(f"Error fetching calendar events: {e}")
        return jsonify({"message": "Internal server error"}), 500
