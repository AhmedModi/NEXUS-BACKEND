#!/bin/sh
set -e

echo "[entrypoint] Applying database migrations..."
python backend/manage.py migrate --noinput

echo "[entrypoint] Collecting static files..."
python backend/manage.py collectstatic --noinput || true

echo "[entrypoint] Starting Gunicorn..."
exec gunicorn backend.wsgi:application --bind 0.0.0.0:8000 --workers ${WEB_CONCURRENCY:-3}


