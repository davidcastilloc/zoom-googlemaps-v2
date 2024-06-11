#!/bin/sh
source .venv/bin/activate
export FLASK_ENV=production
gunicorn polygon.server:app --bind=localhost:5001