from typing import Dict
from pathlib import Path
from datetime import datetime

from flask import Blueprint, jsonify, request, current_app

from central_microservice.bin.FileManager import SpeedFileManager
from central_microservice.bin.SpeedFile import SpeedFile
from central_microservice.tasks import tasks
from central_microservice.GatemanAPIClient.GatemanAPIClient import (
    Api,
    GatemanApiResponse,
)

central_blueprint = Blueprint("central_blueprint", __name__)


@central_blueprint.route("/central/report/speed", methods=["PUT"])
def retrive_train_speed():
    res: Dict[str, str] = {"status": "OK"}
    if "speed" not in request.get_json():
        res["status"] = "ERROR. Not found speed in request"
        return jsonify(res), 400

    speed_str: str = request.get_json().get("speed")
    speed_float: float = float(speed_str)

    # write to file
    speed_files_dir = Path(current_app.config.get("BASE_DIR"), "speed_files")
    file_path: Path = SpeedFile.get_speed_file_full_path(speed_files_dir, speed_float)
    datetime_now: str = datetime.now().strftime("[%d-%m-%Y %H:%M:%S]")

    with SpeedFileManager(file_path, "a+") as sfm:
        sfm.write(f"{datetime_now} {speed_str}\n")

    return jsonify(res), 200


@central_blueprint.route("/central/report/station", methods=["PUT"])
def retrive_train_station():
    API_BASE_URL: str = current_app.config.get("GATEMAN_API_BASE_URL")
    gateman_api_client: Api = Api(API_BASE_URL)

    station_name: str = request.get_json().get("station")
    current_app.logger.info(f"Pociąg zbliża się do stacji {station_name}")

    # Get barrier status
    resp: GatemanApiResponse = gateman_api_client.get_barrier_state()
    if resp.status_code != 200:
        return jsonify(resp.data_dict), resp.status_code
    barrier_status = 0 if resp.data_dict.get("state") == 0 else 1

    # manage barrier
    if barrier_status:
        resp: GatemanApiResponse = gateman_api_client.close_barrier()
        current_app.logger.info("Szlaban zamknięty")
        if resp.status_code != 200:
            return jsonify(resp.data_dict), resp.status_code
    else:
        current_app.logger.error("Błąd. Szlaban zamkniety. Otwieram za 10 sekund")

    # set task to open barrier after 10 sec
    tasks.send_open_barrier.apply_async((), countdown=10)
    return jsonify({"status": "OK"}), resp.status_code
