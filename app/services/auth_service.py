from flask_jwt_extended import create_access_token
from app.models.user import User

class AuthService:
    @staticmethod
    def login(email, password):
        user = User.find_by_email(email)
        if user and User.verify_password(user['password_hash'], password):
            access_token = create_access_token(identity=str(user['_id']), additional_claims={"role": user['role']})
            return {
                "access_token": access_token,
                "user": {
                    "name": user['name'],
                    "email": user['email'],
                    "role": user['role']
                }
            }, 200
        return {"message": "Invalid credentials"}, 401

    @staticmethod
    def create_staff(admin_id, name, email, password, department=None):
        # Admin check should be done in controller/middleware
        if User.find_by_email(email):
            return {"message": "User already exists"}, 400
        
        User.create_user(name, email, password, "STAFF", department)
        return {"message": "Staff account created successfully"}, 201
