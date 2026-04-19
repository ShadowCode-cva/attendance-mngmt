from functools import wraps
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from flask import jsonify

def role_required(required_role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            # identity contains identity={'id': ..., 'role': ...}
            # get_jwt() returns the full payload including custom claims
            # Identity is stored in 'sub' in standard JWT, but we stored it in identity
            
            user_role = claims.get("role")
            
            if user_role != required_role:
                return jsonify({"message": f"Access restricted to {required_role} only"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
