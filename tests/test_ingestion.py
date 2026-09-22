from datetime import datetime

from src.pipeline.ingestion import (
    IngestionResult,
    ingest_opencity_aqi,
)


CSV_PATH = "fixtures/opencity_alipur_dpcc_2017_2023.csv"


def test_ingestion_result_starts_empty():
    result = IngestionResult(source="test")

    assert result.source == "test"
    assert result.records == []
    assert result.errors == []


def test_ingest_opencity_aqi():
    result = ingest_opencity_aqi(
        file_path=CSV_PATH,
        latitude=28.797226,
        longitude=77.133136,
        station_name="Alipur DPCC",
        start_date=datetime(2019, 10, 25),
        end_date=datetime(2019, 11, 10, 23, 59, 59),
    )

    assert result.source == "CPCB/OpenCity"
    assert not result.errors
    assert len(result.records) == 371
    assert result.records[0].parameter == "AQI"
    assert result.records[0].station_name == "Alipur DPCC"