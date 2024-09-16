# Environment
Create virtual environment
```
virtualenv .venv
```
#### install requirments
For windows powershell
```
.\.venv\Scripts\activate
pip install --no-cache-dir --ignore-installed -r requirements.txt
$Env:FLASK_APP="flask_app:create_app"
```
For linux/macos
```
.\.venv\bin\activate
pip install --no-cache-dir --ignore-installed -r requirements.txt
$Env:FLASK_APP="flask_app:create_app"
export FLASK_APP="flask_app:create_app"
```
## using macros
For windows powershell
```
build_env.ps1
set_env.ps1
```
For linux/macos
```
sh ./build_env.sh
source ./set_env.sh
```
# App environment settings
### using app-env file

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

# Database cli
```
flask db init -m "init"
flask db migrate
flask db upgrade
```
# Start server for develope
For windows powershell
```
start_server.ps1
```
For linux/macos
```
./start_server.sh
```
# Deployment
```
docker-compose --env-file app-env up -d
```

# OpenSSL
```
openssl req -x509 -new -nodes -sha256 -utf8 -days 3650 -newkey rsa:2048 -keyout ssl.key -out server.crt -config ssl.conf
```