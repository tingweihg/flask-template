import click
from flask import Flask
from flask_app.config import BaseConfig
from flask_app.extensions.database import db
from flask_app.auth.models.user import User
from flask_app.auth.models.role import UserRole


def init_app_command(app):
    

    @app.cli.command("app-info")
    def show_version():
        '''Show app information'''
        print("{} {}".format(BaseConfig().app_env['APP_NAME'], BaseConfig().app_env['APP_VERSION']))
        
    @app.cli.command("app-name")
    def show_version():
        '''Show app name'''
        print("{}".format(BaseConfig().app_env['APP_NAME']))
        
    @app.cli.command("app-version")
    def show_version():
        '''Show version'''
        print("{}".format(BaseConfig().app_env['APP_VERSION']))


    # initialize database
    @app.cli.command("init-db")
    def init_db():
        '''Initialize database'''
        db.create_all()
        print("Database initialized.")

    # add user
    @app.cli.command("user-add")
    @click.option("-u", "--user_name", "user_name", required=True, help="User name")
    @click.option("-p", "--password", "password", required=True, help="User password")
    @click.option("-r", "--role", "role", type=click.Choice(UserRole.choices()), required=True, help="User password")
    def add_user(user_name, password, role): 
        '''Add user'''
        return User.add_user(user_name, password, role)
    
    @app.cli.command("user-delete")
    @click.option("-u", "--user_name", "user_name", required=True, help="User name")
    def delete_user(user_name):
        '''Delete user'''
        User.delete_from_db(user_name)

    @app.cli.command("user-update")
    @click.option("-u", "--user_name", "user_name", required=True, help="User name")
    @click.option("-p", "--password", "password", help="User password")
    @click.option("-r", "--role", "role", type=click.Choice(UserRole.choices()), help="User role")
    def update_user(user_name, password, role):
        '''Update user'''
        User.update_user(user_name, password, role)

    
    @app.cli.command("user-set-role")
    @click.option("-u", "--user_name", "user_name", required=True, help="User name")
    @click.option("-r", "--role", "role", required=True, type=click.Choice(UserRole.choices()), help="User role")
    def update_user(user_name, role):
        '''Set user role'''
        User.update_user(user_name, None, role)
        
    
    @app.cli.command("user-set-password")
    @click.option("-u", "--user_name", "user_name", required=True, help="User name")
    @click.option("-p", "--password", "password", required=True, help="User password")
    def update_user(user_name, password):
        '''Set user password'''
        User.update_user(user_name, password, None)

    # show all users
    @app.cli.command("user-show-all")
    def show_all_users():
        '''Show users'''
        users = User.get_user_list()
        for user in users:
            print("{} (id: {}, role: {})".format(user.user_name, user.id, user.role.role_name))

    # show user
    @app.cli.command("user-show")
    @click.option("-u", "--user_name", "user_name", required=True, help="User name")
    def show_user(user_name):
        '''Search role'''
        user = User.get_by_user_name(user_name)
        if user == None:
            print("User({}) not found.".format(user_name))
        else:
            print("{} (id: {}, role: {})".format(user.user_name, user.id, user.role.role_name))

    # show roles    
    @app.cli.command("role-show-all")
    def show_roles():
        '''Show roles'''
        roles = UserRole.get_roles()
        for role in roles:
            print("{}: {}".format(role.id, role.role_name))
        
    
    user_roles = UserRole.get_roles()
    for role in user_roles:
        @app.cli.command("role-show-all-{}".format(role.role_name))
        def show_role():
            '''Show users by role'''
            users = User.get_by_role('admin')
            for user in users:
                print("{} (id: {}, role: {})".format(user.user_name, user.id, user.role.role_name))