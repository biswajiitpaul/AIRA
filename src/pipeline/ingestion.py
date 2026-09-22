from src.adapters.opencity_delhi import parse_opencity_aqi
from dataclasses import dataclass, field
from typing import Any, List

from src.adapters.open_aq import get_latest_air_quality, normalize_air_quality
from src.adapters.open_meteo import get_weather
from src.adapters.nasa_firms import get_fire_data


@dataclass
class IngestionResult:
    source: str
    records: List[Any] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


def ingest_open_aq(location_id: int) -> IngestionResult:
    result = IngestionResult(source="OpenAQ")

    try:
        data = get_latest_air_quality(location_id)
        result.records.append(normalize_air_quality(data))
    except Exception as exc:
        result.errors.append(str(exc))

    return result


def ingest_weather(latitude: float, longitude: float) -> IngestionResult:
    result = IngestionResult(source="Open-Meteo")

    try:
        data = get_weather(latitude, longitude)
        result.records.append(data)
    except Exception as exc:
        result.errors.append(str(exc))

    return result


def ingest_fire_data(
    west: float,
    south: float,
    east: float,
    north: float,
    day_range: int = 1,
) -> IngestionResult:
    result = IngestionResult(source="NASA FIRMS")

    try:
        data = get_fire_data(
            west,
            south,
            east,
            north,
            day_range=day_range,
        )
        result.records.append(data)
    except Exception as exc:
        result.errors.append(str(exc))

    return result
def ingest_opencity_aqi(
    file_path: str,
    latitude: float,
    longitude: float,
    station_name: str,
    start_date=None,
    end_date=None,
) -> IngestionResult:
    result = IngestionResult(source="CPCB/OpenCity")

    try:
        records = parse_opencity_aqi(
            file_path=file_path,
            latitude=latitude,
            longitude=longitude,
            station_name=station_name,
            start_date=start_date,
            end_date=end_date,
        )
        result.records.extend(records)
    except Exception as exc:
        result.errors.append(str(exc))

    return result