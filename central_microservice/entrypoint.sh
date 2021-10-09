#!/bin/bash
source venv/bin/activate
celery -A central_microservice.celery_runner worker -n "central" --loglevel=INFO