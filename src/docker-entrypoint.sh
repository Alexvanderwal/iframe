#!/usr/bin/env bash

python manage.py migrate # Apply all db migrations
python manage.py collectstatic --noinput # Collect all static files

cd ./src
# Stat Gunicorn processes
echo Starting Gunicorn.
exec gunicorn iframe:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
