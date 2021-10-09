import sys
from pathlib import Path

from flask import Flask
from decouple import Config, RepositoryEnv

from gateman.routes import gateman_blueprint
from gateman.db import db
from gateman import utils


def create_application(test: bool = False) -> Flask:
    BASE_DIR: Path = Path(__file__).parent.absolute()
    CONFIG_FILE_PATH: Path = Path(BASE_DIR, "config.ini")

    if not Path.exists(CONFIG_FILE_PATH):
        print(f"Not found config file: {CONFIG_FILE_PATH}")
        exit(-1)

    app: Flask = Flask(__name__)

    file_config: Config = Config(RepositoryEnv(CONFIG_FILE_PATH))
    app.config["SECRET_KEY"] = file_config.get("SECRET_KEY", cast=str)
    app.config["APP_PORT"] = file_config.get("APP_PORT", cast=int)
    app.config["TESTING"] = test
    app.config["DEBUG"] = file_config.get("DEBUG", cast=bool)

    # Init and populate db
    if not test:
        app.config["SQLALCHEMY_DATABASE_URI"] = file_config.get(
            "SQLALCHEMY_DATABASE_URI"
        )
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

        db.init_app(app)
        with app.app_context():
            db.create_all()
            utils.populate_barrier(db)

    app.register_blueprint(gateman_blueprint)

    return app


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
