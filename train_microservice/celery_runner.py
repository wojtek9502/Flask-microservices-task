from pathlib import Path

from celery import Celery
from decouple import Config, RepositoryEnv


def get_config(path: Path) -> Config:
    if not Path.exists(path):
        print(f"Not found config file: {path}")
        exit(-1)
    file_config: Config = Config(RepositoryEnv(path))
    return file_config


BASE_DIR: Path = Path(__file__).parent.absolute()
CONFIG_FILE_PATH: Path = Path(BASE_DIR, "config.ini")
config: Config = get_config(CONFIG_FILE_PATH)
CENTRAL_MICROSERVICE_URL = config.get("CENTRAL_MICROSERVICE_URL", cast=str)

celery = Celery("celery_runner", include=["train_microservice.tasks.tasks"])

celery.conf.update(
    broker_url="amqp://",
    backend_url="rpc://",
    task_serializer="json",
    accept_content=["json"],  # Ignore other content
    result_serializer="json",
    timezone="Europe/Warsaw",
    enable_utc=True,
)

celery.conf.beat_schedule = {
    "train_speed_task": {
        "task": "train_microservice.tasks.tasks.send_train_speed_info",
        "schedule": 10.0,
        "options": {"queue": "celery_periodic"},
    },
    "train_station_task": {
        "task": "train_microservice.tasks.tasks.send_nearest_station_info",
        "schedule": 180.0,
        "options": {"queue": "celery_periodic"},
    },
}
