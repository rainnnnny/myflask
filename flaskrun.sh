#!/bin/bash
export FLASK_APP=./main/main.py
export FLASKR_SETTINGS=./main/config.py
flask run --port=5000 --host=127.0.0.1
