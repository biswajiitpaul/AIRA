import os
import requests
from dotenv import load_dotenv

load_dotenv()


def get_fire_data(
    west,
    south,
    east,
    north,
    source="VIIRS_NOAA20_NRT",
    day_range=1,
):
    map_key = os.getenv("NASA_FIRMS_MAP_KEY")

    if not map_key:
        raise RuntimeError("NASA_FIRMS_MAP_KEY is not set")

    area = f"{west},{south},{east},{north}"

    url = (
        f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/"
        f"{map_key}/{source}/{area}/{day_range}"
    )

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    return response.text