from flask import Flask
from .config import Config, DevConfig, BaseConfig
from .extensions import db, migrate, login_manager, my_logger, jwt


def create_app(dev = False):

    config = Config()
    if dev is True:
        config = DevConfig

    # set app configurations
    app = Flask(config.app_env["APP_NAME"], template_folder='templates')
    app.config.from_object(config)


    # initialize app 
    db.init_app(app)
    my_logger.init_app(app, dev)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    jwt.init_app(app)
    
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
        
    
    with app.app_context():
        
        # 非常重要! 否則會出現 RuntimeError: Working outside of application context.
        from .auth.models import User
        from .api.auth import auth_blueprint

        # register blueprint
        app.register_blueprint(auth_blueprint)


    # done, start application
    app.logger.info("Application started.")
    return app

