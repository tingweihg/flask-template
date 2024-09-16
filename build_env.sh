#!/bin/bash

virtualenv .venv
source .venv/bin/activate
export FLASK_APP="flask_app:create_app"
pip install --no-cache-dir --ignore-installed -r requirements.txt
