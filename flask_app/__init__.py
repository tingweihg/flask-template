from flask import Flask
from .config import Config, DevConfig

# extensions
from .extensions.auth import jwt
from .extensions.database import db, migrate
from .extensions.login import login_manager 
from .extensions.logger import my_logger


def helloworld():
    return "Hello World"



def create_app(dev = False):

    config = None
    if dev is True:
        config = DevConfig()
    else:
        config = Config()


    # set app configurations
    app = Flask(config.app_env["APP_NAME"], template_folder='templates')
    app.config.from_object(config)


    # initialize app 
    db.init_app(app)
    my_logger.init_app(app, dev)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    jwt.init_app(app)
        
    
    with app.app_context():
        
        from flask_app.auth.models.role import UserRole
        from flask_app.auth.models.user import User

        db.create_all()
        
        # import all models
        from .extensions.command import init_app_command
        from .extensions.database import (init_user_role, 
                                          init_default_users)
        
        # init user and user role
        init_user_role(app)
        init_default_users(app)
        
        # import api blueprint
        from flask_app.api import api_blueprint
        app.register_blueprint(api_blueprint)

        # for develope
        app.add_url_rule("/", "helloworld", helloworld) 

        # init command
        init_app_command(app)
        
        # print all routes
        # for rule in app.url_map.iter_rules():
            # print(f"Endpoint: {rule.endpoint}, URL: {rule}")


    # done, start application
    app.logger.info("Application started.")
    return app

