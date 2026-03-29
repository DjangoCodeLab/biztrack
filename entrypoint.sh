#!/bin/sh

echo "Waiting for DB..."

while ! nc -z db 5432; do
  sleep 1
done


echo "Applying make migrations..."
python manage.py makemigrations

echo "Applying migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting server..."
gunicorn biztech.wsgi:application --bind 0.0.0.0:8000 --reload