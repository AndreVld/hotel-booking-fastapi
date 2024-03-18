#!/bin/bash


if [[ "${1}" == "celery" ]]; then
    celery --app=app.tasks.celery_conf:celery_app worker -l INFO
elif [[ "${1}" == "celery_beat" ]]; then
    celery --app=app.tasks.celery_conf:celery_app worker -l INFO -B
elif [[ "${1}" == "flower" ]]; then
    celery --app=app.tasks.celery_conf:celery_app flower
fi
