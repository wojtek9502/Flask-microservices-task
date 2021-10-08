from celery import Celery

celery = Celery('central_microservice.app', include=['central_microservice.tasks.tasks'])
celery.conf.update(
    broker_url="amqp://",
    task_serializer="json",
    accept_content=["json"],  # Ignore other content
    result_serializer="json",
    timezone="Europe/Warsaw",
    enable_utc=True,
)