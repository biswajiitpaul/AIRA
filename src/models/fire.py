from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class NormalizedFire:
    latitude: float
    longitude: float
    timestamp: datetime
    brightness: Optional[float] = None
    confidence: Optional[str] = None
    satellite: Optional[str] = None
    instrument: Optional[str] = None