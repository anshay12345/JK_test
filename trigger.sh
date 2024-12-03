#!/bin/sh
fuser -k 8000/tcp
python manage.py collectstatic
uvicorn chatbot.asgi:application --host 0.0.0.0 --port 8000