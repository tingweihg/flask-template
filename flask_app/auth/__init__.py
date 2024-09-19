from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask_login import current_user

from flask_app.extensions.auth import jwt


def jwt_role_required(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            
            # check jwt token
            from flask_app.auth.models.user import User
            verify_jwt_in_request()
            identity = get_jwt_identity()
            user = User.get_by_user_name(identity)
            role = user.role.role_name
            if role not in roles:
                return jsonify({'message': 'Permission denied!'}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator




def login_role_required(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                return jsonify({'message': 'Login required!'}), 401
            role = current_user.role.role_name
            if role not in roles:
                return jsonify({'message': 'Permission denied!'}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator