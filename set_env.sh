#!/bin/bash

# Activate the virtual environment
if [ -d ".venv/bin" ]; then
    source .venv/bin/activate
else
    echo "Virtual environment not found. Please create it first."
    exit 1
fi

# Set the FLASK_APP environment variable
export FLASK_APP="flask_app:create_app"

echo "Virtual environment activated and FLASK_APP set."