from flask_app import create_app
from flask_app.extensions import db

if __name__ == '__main__':

    app = create_app(True)
    app.run(debug=True, port="5001", host="0.0.0.0")