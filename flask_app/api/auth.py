from flask import Blueprint, request, jsonify, current_app
from flask_app.auth.models import User
from flask_jwt_extended import (create_access_token, create_refresh_token, set_access_cookies, unset_jwt_cookies, 
                                get_jwt_identity, jwt_required, set_refresh_cookies, get_jwt)
from flask_app.extensions.auth import jwt
from datetime import datetime, timezone, timedelta
from time import strftime, localtime

auth_blueprint = Blueprint("auth", __name__, url_prefix="/api/auth")



# login
def login():
    user_name = request.json.get("user_name", None)
    password = request.json.get("password", None)

    # check if user_name and password is None
    if user_name is None or password is None:
        return jsonify({"msg": "Bad username or password", "status":"400"}), 400

    # check if user exists and password is correct
    user = User.get_by_username(user_name)
    if not user or not user.check_password(password):
        return jsonify({"msg": "Bad username or password", "status":401}), 401

    # create access token
    access_token = create_access_token(identity=user_name, expires_delta=current_app.config["JWT_EXPIRATION_DELTA"])
    refresh_token = create_refresh_token(identity=user_name, expires_delta=current_app.config["JWT_REFRESH_TOKEN_EXPIRES"])
    
    response = jsonify(status=200, 
                       msg="Login successful for {}.".format(user_name), 
                       time=datetime.now(timezone.utc).isoformat(),
                       access_token=access_token,
                       user_name=user_name) 
    
    # set access token to cookie
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    
    current_app.logger.info("Login successful for {}.".format(user_name))
    return response, 200

# logout
@jwt_required()
def logout():
    identity = get_jwt_identity()
    response = jsonify(status=200, 
                       msg="Logout successful for {}.".format(identity), 
                       time=datetime.now(timezone.utc).isoformat()) 
    unset_jwt_cookies(response)
    response.delete_cookie("access_token")
    return response, 200


# auto refresh token
@current_app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + current_app.config["JWT_EXPIRATION_DELTA"]/3)

        if target_timestamp > exp_timestamp:
            identity = get_jwt_identity()
            access_token = create_access_token(identity=identity, expires_delta=current_app.config["JWT_EXPIRATION_DELTA"])
            set_access_cookies(response, access_token)
            current_app.logger.info("Auto refresh access token for {}.".format(identity))
    except (RuntimeError, KeyError):
        pass
    return response


# manual refresh
@jwt_required(refresh=True, locations=["cookies"])
def refresh():    
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, expires_delta=current_app.config["JWT_EXPIRATION_DELTA"])
    response = jsonify(status=200, 
                       msg="Login successful.", 
                       time=datetime.now(timezone.utc).isoformat(),
                       access_token=access_token,
                       user_name=identity) 
    set_access_cookies(response, access_token)
    current_app.logger.info("Refresh token for {}.".format(identity))
    return response, 200


# unauthorized
@jwt.unauthorized_loader
def unauthorized_response(callback):
    response = jsonify(status=401, 
                       msg="Please login first.", 
                       time=datetime.now(timezone.utc).isoformat()) 
    return response, 401


# who am i
@jwt_required()
def who_am_i():
    response = jsonify(status=200, 
                       msg="You are {}.".format(get_jwt_identity()), 
                       time=datetime.now(timezone.utc).isoformat()) 
    return response, 200



    
# login
auth_blueprint.route("/login", methods=["POST"])(login)
auth_blueprint.route("/logout", methods=["GET"])(logout)
auth_blueprint.route("/refresh", methods=["POST"])(refresh)
auth_blueprint.route("/who_am_i", methods=["GET"])(who_am_i)
