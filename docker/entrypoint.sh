#!/bin/bash
cd /app/src
python manage.py migrate
python manage.py set_admin_bot_webhook
gunicorn --bind 0.0.0.0:8000 config.wsgi
