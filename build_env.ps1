virtualenv .venv
.\.venv\Scripts\activate
$Env:FLASK_APP="flask_app:create_app"
pip install --no-cache-dir --ignore-installed -r requirements.txt
