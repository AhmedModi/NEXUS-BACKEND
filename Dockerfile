FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system packages (minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser:appuser /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app/

USER appuser

ENV DJANGO_SETTINGS_MODULE=backend.settings
ENV PYTHONPATH=/app/backend

ENTRYPOINT ["/app/backend/entrypoint.sh"]
