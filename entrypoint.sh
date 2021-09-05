#!/bin/bash

set -e

echo "{0}: running database migrations."
python manage.py migrate --no-input

echo "{0}: collecting static files."
python manage.py collectstatic --no-input

gunicorn cluesolver.wsgi --bind 0.0.0.0:8000 --reload
