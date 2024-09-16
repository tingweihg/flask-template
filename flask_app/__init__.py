from flask import Flask
from .config import Config, DevConfig

# extensions
from .extensions.auth import jwt
from .extensions.database import db, migrate
from .extensions.login import login_manager 
from .extensions.logger import my_logger
from .extensions.command import init_app_command


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

        db.create_all()
        
        # 非常重要! 否則會出現 RuntimeError: Working outside of application context.
        from .auth.models import User
        from .api.auth import auth_blueprint

        # register blueprint
        app.register_blueprint(auth_blueprint)

        # for develope
        app.add_url_rule("/", "helloworld", helloworld) 

        # init command
        init_app_command(app)


    # done, start application
    app.logger.info("Application started.")
    return app

