#./bin/bash

# Activate the existing virtual environment
source ../search-engine-venv/bin/activate  # On macOS and Linux
# source ../search-engine-venv/Scripts/activate  # On Windows (Git Bash)

# Set the FLASK_APP environment variable
export FLASK_APP=./index.py

# Run the Flask application within the activated virtual environment
flask run -h 0.0.0.0
