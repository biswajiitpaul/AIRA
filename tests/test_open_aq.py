import json
from pathlib import Path

from src.adapters.open_aq import normalize_air_quality


def test_normalize_air_quality():
    fixture_path = Path("fixtures/open_aq_latest_8118.json")

    with fixture_path.open(encoding="utf-8") as file:
        data = json.load(file)

    result = normalize_air_quality(data)

    assert result.latitude == data["results"][0]["coordinates"]["latitude"]
    assert result.longitude == data["results"][0]["coordinates"]["longitude"]
    assert result.value == data["results"][0]["value"]
    assert result.sensor_id == data["results"][0]["sensorsId"]
    assert result.location_id == data["results"][0]["locationsId"]