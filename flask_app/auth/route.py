from flask import Blueprint, redirect, url_for
from flask_app.extensions import login_manager

auth_blueprint = Blueprint("auth", __name__, url_prefix="/")


