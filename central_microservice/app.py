from pathlib import Path

from celery import Celery
from flask import Flask

from decouple import Config, RepositoryEnv


def make_celery(app) -> Celery:
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


def create_application() -> Flask:
    BASE_DIR: Path = Path(__file__).parent.absolute()
    CONFIG_FILE_PATH: Path = Path(BASE_DIR, "config.ini")

    if not Path.exists(CONFIG_FILE_PATH):
        print(f"Not found config file: {CONFIG_FILE_PATH}")
        exit(-1)

    app: Flask = Flask(__name__)

    file_config: Config = Config(RepositoryEnv(CONFIG_FILE_PATH))
    app.config["APP_IP"] = file_config.get("APP_IP", cast=str)
    app.config["APP_PORT"] = file_config.get("APP_PORT", cast=int)
    app.config["SECRET_KEY"] = file_config.get("SECRET_KEY", cast=str)
    app.config["TESTING"] = file_config.get("TESTING", cast=bool)
    app.config["DEBUG"] = file_config.get("DEBUG", cast=bool)

    # Celery
    app.config['CELERY_BROKER_URL'] = file_config.get("CELERY_BROKER_URL", cast=str)
    app.config['CELERY_RESULT_BACKEND'] = file_config.get("CELERY_RESULT_BACKEND", cast=str)

    return app

application = create_application()
celery = make_celery(application)

@celery.task()
def add_together(a, b):
    return a + b

# result = add_together.delay(23, 42)
# result.wait()  # 65


