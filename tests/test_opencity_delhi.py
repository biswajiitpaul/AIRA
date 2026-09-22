from datetime import datetime

from src.adapters.opencity_delhi import parse_opencity_aqi


CSV_PATH = "fixtures/opencity_alipur_dpcc_2017_2023.csv"


def test_parse_october_25_2019():
    records = parse_opencity_aqi(
        CSV_PATH,
        latitude=28.797226,
        longitude=77.133136,
        station_name="Alipur DPCC",
        start_date=datetime(2019, 10, 25),
        end_date=datetime(2019, 10, 25, 23, 59, 59),
    )

    assert records

    assert all(record.parameter == "AQI" for record in records)
    assert all(record.station_name == "Alipur DPCC" for record in records)
    assert all(record.source == "CPCB/OpenCity" for record in records)


def test_locked_demo_window():
    records = parse_opencity_aqi(
        CSV_PATH,
        latitude=28.797226,
        longitude=77.133136,
        station_name="Alipur DPCC",
        start_date=datetime(2019, 10, 25),
        end_date=datetime(2019, 11, 10, 23, 59, 59),
    )

    assert records

    assert min(record.timestamp for record in records) >= datetime(2019, 10, 25)

    assert max(record.timestamp for record in records) <= datetime(
        2019,
        11,
        10,
        23,
        59,
        59,
    )