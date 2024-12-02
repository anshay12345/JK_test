#!/bin/sh
fuser -k 8000/tcp
python manage.py runserver 0.0.0.0:8000
