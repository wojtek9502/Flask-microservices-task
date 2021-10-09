import pytest


@pytest.fixture(scope="session")
def celery_config():
    return {
        "broker_url": "amqp://",
        "result_backend": "db+sqlite:///train_microservice/tests/celery_test_backend.sqlite",
    }
