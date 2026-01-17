from app import app, db
from models import User, Event, Registration

def populate_database():
    with app.app_context():
        # Add admin user if not already present
        if not User.query.filter_by(username='admin1').first():
            admin = User(username='admin1', role='admin')
            admin.set_password('a1pass')  # Password: a1pass
            db.session.add(admin)

        # Add student users if not already present
        for i in range(1, 16):
            if not User.query.filter_by(username=f'student{i}').first():
                student = User(username=f'student{i}', role='student')
                student.set_password(f's{i}pass')  # Password: s1pass, s2pass, etc.
                db.session.add(student)

        # Commit users to ensure they exist before adding registrations
        db.session.commit()

        # Add events if not already present
        events = [
            {'title': 'TechFest 2025', 'date': '2025-04-10'},
            {'title': 'Cultural Night', 'date': '2025-04-15'},
            {'title': 'Hackathon 2025', 'date': '2025-04-20'},
            {'title': 'Tech Talk', 'date': '2025-05-01'},
            {'title': 'Workshop', 'date': '2025-05-10'},
        ]
        for event in events:
            if not Event.query.filter_by(title=event['title']).first():
                new_event = Event(
                    title=event['title'],
                    date=event['date'],
                    tagline="Join us for an unforgettable experience!",  # Default tagline
                    poster_path=None  # No poster by default
                )
                db.session.add(new_event)

        # Commit events to ensure they exist before adding registrations
        db.session.commit()

        # Add registrations if not already present
        registrations = [
            {'user_id': 2, 'event_id': 1},  # Student1 registered for TechFest
            {'user_id': 3, 'event_id': 1},  # Student2 registered for TechFest
            {'user_id': 4, 'event_id': 2},  # Student3 registered for Cultural Night
            {'user_id': 5, 'event_id': 3},  # Student4 registered for Hackathon
            {'user_id': 6, 'event_id': 4},  # Student5 registered for Tech Talk
            {'user_id': 7, 'event_id': 5},  # Student6 registered for Workshop
        ]
        for reg in registrations:
            # Ensure the user and event exist before adding the registration
            user = db.session.get(User, reg['user_id'])  # Use Session.get()
            event = db.session.get(Event, reg['event_id'])  # Use Session.get()
            if user and event:
                if not Registration.query.filter_by(user_id=reg['user_id'], event_id=reg['event_id']).first():
                    new_registration = Registration(user_id=reg['user_id'], event_id=reg['event_id'])
                    db.session.add(new_registration)

        # Commit registrations
        db.session.commit()
        print("Database populated successfully!")

if __name__ == '__main__':
    populate_database()
