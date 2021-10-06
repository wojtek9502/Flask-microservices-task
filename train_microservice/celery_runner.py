from celery import Celery
from .tasks.tasks import send_train_speed_info, send_near_station_info

celery = Celery('celery_runner', include=['train_microservice.tasks.tasks'])

celery.conf.update(
    broker_url='pyamqp://',
    # result_backend='redis://localhost'
)

celery.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
    timezone='Europe/Warsaw',
    enable_utc=True,
)


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, send_train_speed_info.s())
    sender.add_periodic_task(180.0, send_near_station_info.s())
