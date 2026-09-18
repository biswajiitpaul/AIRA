from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class NormalizedWeather:
    latitude: float
    longitude: float
    timestamp: datetime
    temperature_c: Optional[float] = None
    humidity_percent: Optional[float] = None
    wind_speed_kmh: Optional[float] = None