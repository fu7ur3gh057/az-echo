#!/bin/sh

until cd /app/server
do
    echo "Waiting for server volume..."
done


until python manage.py migrate
do
    echo "Waiting for db to be ready..."
    sleep 2
done


python manage.py collectstatic --noinput

# python manage.py createsuperuser --noinput

# for debug
python manage.py runserver 0.0.0.0:8000

#gunicorn server.wsgi:application --bind 0.0.0.0:8000

exec "$@"
