from app import app, db
from models import Registration

def clear_all_registrations():
    with app.app_context():
        # Delete all registrations
        registrations = Registration.query.all()
        print(f"Deleting {len(registrations)} registrations...")  # Debug log
        for registration in registrations:
            db.session.delete(registration)

        db.session.commit()
        print("All registrations cleared successfully!")

if __name__ == '__main__':
    clear_all_registrations()
