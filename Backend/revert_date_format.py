from app import db
from models import Event
from datetime import datetime

def revert_date_format():
    try:
        events = Event.query.all()
        for event in events:
            # Assuming the original format was 'YYYY-MM-DD'
            if isinstance(event.date, str):
                original_date = datetime.strptime(event.date, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
                event.date = original_date
            db.session.add(event)
        db.session.commit()
        print("Date format reverted successfully.")
    except Exception as e:
        print(f"Error reverting date format: {e}")
        db.session.rollback()

if __name__ == "__main__":
    revert_date_format()
