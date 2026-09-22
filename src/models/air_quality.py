from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class NormalizedAirQuality:
    latitude: float
    longitude: float
    timestamp: datetime
    value: float
    parameter: Optional[str] = None
    unit: Optional[str] = None
    sensor_id: Optional[int] = None
    location_id: Optional[int] = None
    station_name: Optional[str] = None
    source: Optional[str] = None