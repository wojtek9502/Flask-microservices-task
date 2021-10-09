import sys
from pathlib import Path

from flask import Flask
from logging import Formatter
from logging.handlers import RotatingFileHandler
from decouple import Config, RepositoryEnv

from central.routes import central_blueprint


def create_application() -> Flask:
    BASE_DIR: Path = Path(__file__).parent.absolute()
    CONFIG_FILE_PATH: Path = Path(BASE_DIR, "config.ini")

    if not Path.exists(CONFIG_FILE_PATH):
        print(f"Not found config file: {CONFIG_FILE_PATH}")
        exit(-1)

    app: Flask = Flask(__name__)

    file_config: Config = Config(RepositoryEnv(CONFIG_FILE_PATH))
    app.config["BASE_DIR"] = BASE_DIR
    app.config["SECRET_KEY"] = file_config.get("SECRET_KEY", cast=str)
    app.config["APP_PORT"] = file_config.get("APP_PORT", cast=int)
    app.config["TESTING"] = file_config.get("TESTING", cast=bool)
    app.config["DEBUG"] = file_config.get("DEBUG", cast=bool)

    # Celery
    app.config["GATEMAN_API_BASE_URL"] = file_config.get("GATEMAN_API_BASE_URL")
    app.config["CELERY_BROKER_URL"] = file_config.get("CELERY_BROKER_URL")

    # Logger
    APP_LOG_FILE_NAME: str = file_config.get("APP_LOG_FILE_NAME")
    APP_LOGGER_PATH: Path = Path(BASE_DIR, APP_LOG_FILE_NAME)
    APP_LOG_FORMAT: str = file_config.get("APP_LOG_FORMAT")
    APP_LOG_LEVEL: str = file_config.get("APP_LOG_LEVEL")

    file_handler: RotatingFileHandler = RotatingFileHandler(
        APP_LOGGER_PATH, maxBytes=1024 * 1024 * 100, backupCount=3
    )
    file_handler.setLevel(APP_LOG_LEVEL)
    formatter: Formatter = Formatter(APP_LOG_FORMAT)
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)

    app.register_blueprint(central_blueprint)
    return app


application = create_application()
if __name__ == "__main__":
    application = create_application()

    ip = "0.0.0.0"
    port = application.config["APP_PORT"]
    if len(sys.argv) == 2:
        ip = sys.argv[1]

    application.run(
        ip,
        port=port,
        debug=application.config["DEBUG"],
    )