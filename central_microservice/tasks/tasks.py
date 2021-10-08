import random
import requests

from train_microservice.celery_runner import celery, CENTRAL_MICROSERVICE_URL
from train_microservice.utils import stations_list


@celery.task()
def send_train_speed_info():
    speed: float = random.uniform(0, 180)
    speed_str = format(speed, ".1f")

    payload = {"speed": speed_str}
    res = requests.put(f'{CENTRAL_MICROSERVICE_URL}/central/report/speed', json=payload)
    return 0

@celery.task()
def send_nearest_station_info():
    random.shuffle(stations_list)
    station_name = stations_list[0]

    payload = {"station": station_name}
    res = requests.put(f'{CENTRAL_MICROSERVICE_URL}/central/report/station', json=payload)
    return 0
