import csv
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from src.models.air_quality import NormalizedAirQuality


MONTHS = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12,
}


def parse_opencity_aqi(
    file_path: str | Path,
    latitude: float,
    longitude: float,
    station_name: str = "Alipur DPCC",
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> List[NormalizedAirQuality]:

    records: List[NormalizedAirQuality] = []

    current_year: Optional[int] = None
    current_month: Optional[int] = None

    with Path(file_path).open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:

        reader = csv.reader(file)

        for row in reader:

            if not row:
                continue

            first = row[0].strip().strip('"')

            if first == "Year":
                if len(row) > 1 and row[1].strip():
                    current_year = int(row[1].strip())
                continue

            if "-" in first:
                month_name, year_text = first.rsplit("-", 1)

                if month_name in MONTHS:
                    current_month = MONTHS[month_name]
                    current_year = int(year_text)
                    continue

            if not first or not first.isdigit():
                continue

            if current_year is None or current_month is None:
                continue

            day = int(first)

            for hour, raw_value in enumerate(row[1:25]):

                raw_value = raw_value.strip()

                if not raw_value:
                    continue

                try:
                    value = float(raw_value)
                except ValueError:
                    continue

                timestamp = datetime(
                    current_year,
                    current_month,
                    day,
                    hour,
                )

                if start_date and timestamp < start_date:
                    continue

                if end_date and timestamp > end_date:
                    continue

                records.append(
                    NormalizedAirQuality(
                        latitude=latitude,
                        longitude=longitude,
                        timestamp=timestamp,
                        value=value,
                        parameter="AQI",
                        unit="index",
                        station_name=station_name,
                        source="CPCB/OpenCity",
                    )
                )

    return records