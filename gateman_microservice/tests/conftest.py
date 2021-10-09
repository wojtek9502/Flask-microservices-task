import os
import tempfile

import pytest
import datetime

from gateman_microservice.app import create_application
from gateman_microservice.gateman.db import db
from gateman_microservice.gateman.models import BarrierModel


@pytest.fixture
def client():
    app = create_application(test=True)
    db_fd, db_path = tempfile.mkstemp()
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    barrier_obj = BarrierModel(state=0, last_modify=datetime.datetime(2021, 1, 1))

    with app.test_client() as client:
        db.init_app(app)
        with app.app_context():
            db.create_all()
            if not BarrierModel.query.get(1):
                db.session.add(barrier_obj)
                db.session.commit()
        yield client

    os.close(db_fd)
    os.unlink(db_path)
