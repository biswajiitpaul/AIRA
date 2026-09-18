import os

import requests
from dotenv import load_dotenv


load_dotenv()


def get_latest_air_quality(location_id):
    api_key = os.getenv("OPENAQ_API_KEY")

    if not api_key:
        raise RuntimeError("OPENAQ_API_KEY is not set")

    url = f"https://api.openaq.org/v3/locations/{location_id}/latest"

    headers = {
        "X-API-Key": api_key,
    }

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    return response.json()

from datetime import datetime

from src.models.air_quality import NormalizedAirQuality


def normalize_air_quality(data):
    result = data["results"][0]

    coordinates = result["coordinates"]

    return NormalizedAirQuality(
        latitude=coordinates["latitude"],
        longitude=coordinates["longitude"],
        timestamp=datetime.fromisoformat(result["datetime"]["utc"].replace("Z", "+00:00")),
        value=result["value"],
        sensor_id=result["sensorsId"],
        location_id=result["locationsId"],
    )