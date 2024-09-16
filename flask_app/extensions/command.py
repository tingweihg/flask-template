import click
from flask import Flask
from flask_app.extensions.database import db
from flask_app.auth.models import User


def init_app_command(app):

    # initialize database
    @app.cli.command("init-db")
    def init_db():
        '''Initialize database'''
        db.create_all()
        print("Database initialized.")

    # add user
    @app.cli.command("add-user")
    @click.option("-u", "--user_name", "user_name", required=True, help="User name")
    @click.option("-p", "--password", "password", required=True, help="User password")
    def add_user(user_name, password): 
        '''Add user'''
        return User.add_user(user_name, password)

    return app