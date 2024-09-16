#!/bin/bash

source .venv/bin/activate
export FLASK_APP="flask_app:create_app"
python run_server.py