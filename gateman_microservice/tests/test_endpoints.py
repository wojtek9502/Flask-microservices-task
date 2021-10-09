import datetime
from typing import Dict

import pytest


@pytest.mark.parametrize(
    "endpoint_url, method, status_code",
    [
        ("gateman/barrier", "get", 200),
        ("gateman/barrier/open", "put", 200),
        ("gateman/barrier/close", "put", 200),
        ("wrong/endpoint", "get", 404),
        ("gateman/barrier/open", "get", 405),  # method not allowed
    ],
)
def test_api_endpoints_endpoint_availability(client, endpoint_url: str, method: str, status_code: int):
    expected: int = status_code

    rv = client.get(endpoint_url)
    if method == "put":
        rv = client.put(endpoint_url)

    assert rv.status_code == expected


def test_barrier_status_endpoint_received_data(client):
    endpoint_url: str = "gateman/barrier"
    datetime_str: str = datetime.datetime(2021, 1, 1).strftime(
        "%a, %d %b %Y %H:%M:%S GMT"
    )
    expected: Dict = {"last_modify": datetime_str, "state": 0}

    rv = client.get(endpoint_url)
    endpont_data: Dict = rv.get_json()

    assert endpont_data == expected


def test_barrier_open_endpoint_received_data(client):
    endpoint_url: str = "gateman/barrier/open"
    expected: int = 1

    rv = client.put(endpoint_url)
    barrier_status: int = rv.get_json().get("state")

    assert barrier_status == expected


def test_barrier_open_endpoint_received_data(client):
    endpoint_url: str = "gateman/barrier/close"
    expected = 0

    rv = client.put(endpoint_url)
    barrier_status = rv.get_json().get("state")

    assert barrier_status == expected
