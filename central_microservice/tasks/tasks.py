import json

from flask import current_app
from celery import shared_task

from GatemanAPIClient.GatemanAPIClient import (
    Api,
    GatemanApiResponse,
)


@shared_task()
def send_open_barrier():
    GATEMAN_API_BASE_URL: str = current_app.config.get("GATEMAN_API_BASE_URL")
    res: GatemanApiResponse = Api(GATEMAN_API_BASE_URL).open_barrier()
    current_app.logger.info("Szlaban otwarty")
    return json.dumps(res.data_dict)
