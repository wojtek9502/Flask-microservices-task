from celery import Celery

from central_microservice.app import application


def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config["CELERY_BROKER_URL"],
        include=["central_microservice.tasks.tasks"],
    )

    celery.conf.update(
        broker_url="amqp://",
        task_serializer="json",
        accept_content=["json"],  # Ignore other content
        result_serializer="json",
        timezone="Europe/Warsaw",
        enable_utc=True,
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery(application)
