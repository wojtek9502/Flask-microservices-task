from requests import Response

from train_microservice.tasks.tasks import (
    send_train_speed_info,
    send_nearest_station_info,
)

# Run central microservice first. Make sure that rabbitqm is running
def test_sending_train_speed_task_integration(celery_app, celery_worker):
    expected = {"status": "OK"}

    res: Response = send_train_speed_info.delay().get(timeout=10)

    assert res.json() == expected
    assert res.status_code == 200


# Run central and gateman microservices first. Make sure that rabbitqm is running
def test_sending_station_name_task_integration(celery_app, celery_worker):
    expected = {"status": "OK"}

    res: Response = send_nearest_station_info.delay().get(timeout=20)

    assert res.json() == expected
    assert res.status_code == 200
