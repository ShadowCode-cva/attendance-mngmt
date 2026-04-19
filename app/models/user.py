from datetime import datetime
from app import mongo, bcrypt

class User:
    @staticmethod
    def create_user(name, email, password, role, department=None):
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        user = {
            "name": name,
            "email": email,
            "password_hash": password_hash,
            "role": role, # ADMIN or STAFF
            "department": department,
            "is_active": True,
            "created_at": datetime.utcnow()
        }
        return mongo.db.users.insert_one(user)

    @staticmethod
    def find_by_email(email):
        return mongo.db.users.find_one({"email": email})

    @staticmethod
    def verify_password(stored_hash, password):
        return bcrypt.check_password_hash(stored_hash, password)
