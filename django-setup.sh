#!/usr/bin/env bash
python /code/backend/manage.py migrate
python /code/backend/manage.py runserver 0.0.0.0:8000