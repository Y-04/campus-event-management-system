from app import app, db
from models import User
from werkzeug.security import generate_password_hash

def hash_existing_passwords():
    with app.app_context():
        users = User.query.all()
        for user in users:
            if not user.password.startswith('scrypt:'):  # Check if the password is already hashed
                print(f"Hashing password for user: {user.username}")
                user.password = generate_password_hash(user.password)
        db.session.commit()
        print("Passwords hashed successfully!")

if __name__ == '__main__':
    hash_existing_passwords()
