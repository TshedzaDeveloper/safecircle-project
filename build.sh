#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p media
mkdir -p staticfiles

# Collect static files
python manage.py collectstatic --no-input

# Run database migrations
python manage.py migrate 