import dataclasses
from typing import Dict

import requests


@dataclasses.dataclass
class GatemanApiResponse:
    data_dict: Dict
    status_code: int


class Api:
    def __init__(self, api_url):
        self.url: str = api_url

    def get_barrier_state(self) -> GatemanApiResponse:
        url = f"{self.url}/gateman/barrier"
        try:
            r = requests.get(url)
            r.raise_for_status()
            return GatemanApiResponse(r.json(), r.status_code)
        except (
            requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.RequestException,
        ) as err:
            dict_ = {"error": str(err)}
            return GatemanApiResponse(dict_, 500)

    def close_barrier(self):
        url = f"{self.url}/gateman/barrier/close"
        try:
            r = requests.put(url)
            r.raise_for_status()
            return GatemanApiResponse(r.json(), r.status_code)
        except (
            requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.RequestException,
        ) as err:
            dict_ = {"error": str(err)}
            return GatemanApiResponse(dict_, 500)

    def open_barrier(self):
        url = f"{self.url}/gateman/barrier/open"
        try:
            r = requests.put(url)
            r.raise_for_status()
            return GatemanApiResponse(r.json(), r.status_code)
        except (
            requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.RequestException,
        ) as err:
            dict_ = {"error": str(err)}
            return GatemanApiResponse(dict_, 500)
