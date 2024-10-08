from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import (create_access_token, create_refresh_token, set_access_cookies, unset_jwt_cookies, 
                                get_jwt_identity, jwt_required, set_refresh_cookies, get_jwt)
from datetime import datetime, timezone, timedelta
from time import strftime, localtime

from flask_app.auth.models.user import User
from flask_app.extensions.auth import jwt
from flask_app.utils.utils import create_response


auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")




# login
def login():
    user_name = request.json.get("user_name", None)
    password = request.json.get("password", None)

    # check if user_name and password is None
    if user_name is None or password is None:
        return jsonify({"msg": "Bad username or password", "status":"400"}), 400

    # check if user exists and password is correct
    user = User.get_by_user_name(user_name)
    if not user or not user.check_password(password):
        return jsonify({"msg": "Bad username or password", "status":401}), 401

    # create access token
    access_token = create_access_token(identity=user_name, expires_delta=current_app.config["JWT_EXPIRATION_DELTA"])
    refresh_token = create_refresh_token(identity=user_name, expires_delta=current_app.config["JWT_REFRESH_TOKEN_EXPIRES"])
    
    response = create_response(status=200,
                               msg="Login successful ({}).".format(user_name),
                               access_token=access_token,
                               user_name=user_name)
    
    # set access token to cookie
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    
    current_app.logger.info("Login successful ({}).".format(user_name))
    return response, 200

# logout
@jwt_required()
def logout():
    identity = get_jwt_identity()    
    response = create_response(status=200, msg="Logout successful ({}).".format(identity))
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
            current_app.logger.info("Auto refresh access token ({}).".format(identity))
    except (RuntimeError, KeyError):
        pass
    return response


# manual refresh
@jwt_required(refresh=True, locations=["cookies"])
def refresh():    
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, expires_delta=current_app.config["JWT_EXPIRATION_DELTA"])
    response = create_response(status=200,
                               msg="Login successful ({}).".format(identity),
                               access_token=access_token,
                               user_name=identity)
    
    set_access_cookies(response, access_token)
    current_app.logger.info("Refresh token ({}).".format(identity))
    return response, 200


# unauthorized
@jwt.unauthorized_loader
def unauthorized_response(callback):
    response = create_response(status=401, msg="Please login first.")
    return response, 401


# who am i
@jwt_required()
def who_am_i():
    response = create_response(status=200, msg="You are {}.".format(get_jwt_identity()))
    return response, 200



    
# login
auth_blueprint.route("/login", methods=["POST"])(login)
auth_blueprint.route("/logout", methods=["GET"])(logout)
auth_blueprint.route("/refresh", methods=["POST"])(refresh)
auth_blueprint.route("/who_am_i", methods=["GET"])(who_am_i)
