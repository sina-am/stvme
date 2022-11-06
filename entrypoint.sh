#!/bin/sh

if [ -f ".env.production" ]; then
    cp .env .env.dev && cp .env.production .env
fi

python /app/manage.py collectstatic --noinput
python /app/manage.py migrate
gunicorn --config /app/config/gunicorn.conf.py
