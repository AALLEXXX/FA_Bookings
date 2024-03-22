#!/bin/sh

until timeout 5s poetry run celery -A app.tasks.conf_celery:celery_worker inspect ping; do
    >&2 echo "Celery workers not available"
done

echo 'Starting flower'
poetry run celery -A app.tasks.conf_celery:celery_worker flower --loglevel=info --broker=redis://redis:6379/0
# "celery", "-A" ,"src.app.celery", "flower", "--port=5555", "--broker=redis://redis:6379/0"
