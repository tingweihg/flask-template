# Environment
Create virtual environment.
```
virtualenv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```
Set environment variables.
For powershell
```
$Env:FLASK_APP="flask_app:create_app"
```

For linux/macos
```
export FLASK_APP="flask_app:create_app"
```

# App settings
app-env

\# app 
APP_NAME = flask_template
APP_VERSION = 0.1
USER = user
PASSWORD = password

\# database
POSTGRES_DB = flask_template
POSTGRES_HOST = host
POSTGRES_PORT = port
POSTGRES_USER = user
POSTGRES_PASSWORD = password

\# pgadmin
PGADMIN_EMAIL = email
PGADMIN_PASSWORD = password

# Database
```
flask db init -m "init"
flask db migrate
flask db upgrade
```

# Deployment
```
docker-compose --env-file app-env up -d
```

# OpenSSL
```
openssl req -x509 -new -nodes -sha256 -utf8 -days 3650 -newkey rsa:2048 -keyout ssl.key -out server.crt -config ssl.conf
```