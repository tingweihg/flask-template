import os
import sys

sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.abspath(os.pardir))

from flask_app import create_app

application = create_app()