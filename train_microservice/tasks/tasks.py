import random

from celery import shared_task

from train_microservice.utils import stations_list



@shared_task
def send_train_speed_info():
    speed = random.uniform(0, 180)
    print(speed)


@shared_task
def send_near_station_info():
    station_name = random.shuffle(stations_list)[0]
    print(station_name)