#!/bin/bash
set -o errexit

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Running Django migrations..."
python manage.py migrate --noinput

echo "Starting Gunicorn..."
exec gunicorn primetel_website.wsgi:application --bind 0.0.0.0:${PORT:-8000}
