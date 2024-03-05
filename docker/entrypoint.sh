#!/bin/bash
cd /app/src
python manage.py migrate
gunicorn --bind 0.0.0.0:8000 config.wsgi
