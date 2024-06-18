#!/bin/sh
source .venv/bin/activate
flask --app polygon.server:app --debug run