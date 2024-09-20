import os
from datetime import timedelta
app_dir = os.path.dirname(os.path.abspath(__file__))
pro_dir = os.path.dirname(app_dir)


class BaseConfig:

    app_env = {}
    SECRET_KEY = os.environ.get("SECRET_KEY", "twh-flask-app")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # jwt
    JWT_SECRET_KEY = SECRET_KEY + "-jwt"
    JWT_EXPIRATION_DELTA = timedelta(minutes=20)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=6)
    JWT_AUTH_URL_RULE = '/auth/login'
    JWT_AUTH_HEADER_PREFIX = 'twh-flask-jwt'
    JWT_TOKEN_LOCATION = ["cookies", "headers", "json"]
    JWT_COOKIE_CSRF_PROTECT = False # 沒有這行時，無法使用POST request


    def __init__(self):
        
        # read app-env
        with open(os.path.join(pro_dir, 'app-env'), 'r') as file:
            for line in file:
                line = line.strip()  
                if line and not line.startswith('#'):  
                    key, value = map(str.strip, line.split('=', 1))  
                    self.app_env[key] = value  


class DevConfig(BaseConfig):

    # database
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", "sqlite:///{}".format(os.path.join(pro_dir, "dev.db")))

    def __init__(self) -> None:
        super().__init__()



class Config(BaseConfig):

    # database 
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", "sqlite:///{}".format(os.path.join(pro_dir, "dev.db")))
    
    def __init__(self) -> None:
        super().__init__()



