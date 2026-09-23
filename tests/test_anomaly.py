from datetime import datetime

from src.adapters.opencity_delhi import parse_opencity_aqi
from src.analysis.anomaly import (
    detect_aqi_anomaly,
    find_aqi_anomalies,
)


CSV_PATH = "fixtures/opencity_alipur_dpcc_2017_2023.csv"


def test_detects_high_aqi_anomaly():
    result = detect_aqi_anomaly(
        current_value=180,
        baseline_values=[80, 85, 82, 78, 84, 81, 83],
    )

    assert result.is_anomaly is True
    assert result.current_value == 180
    assert result.z_score > 2


def test_normal_aqi_is_not_anomaly():
    result = detect_aqi_anomaly(
        current_value=84,
        baseline_values=[80, 85, 82, 78, 84, 81, 83],
    )

    assert result.is_anomaly is False


def test_empty_baseline_raises_error():
    try:
        detect_aqi_anomaly(100, [])
        assert False
    except ValueError as error:
        assert str(error) == "baseline_values cannot be empty"


def test_anomaly_with_real_opencity_data():
    records = parse_opencity_aqi(
        file_path=CSV_PATH,
        latitude=28.797226,
        longitude=77.133136,
        station_name="Alipur DPCC",
        start_date=datetime(2019, 10, 25),
        end_date=datetime(2019, 11, 10, 23, 59, 59),
    )

    values = [record.value for record in records]

    baseline = values[:-1]
    current_value = values[-1]

    result = detect_aqi_anomaly(
        current_value=current_value,
        baseline_values=baseline,
    )

    assert result.current_value == current_value
    assert result.baseline_mean > 0
def test_find_aqi_anomalies_with_real_data():
    records = parse_opencity_aqi(
        file_path=CSV_PATH,
        latitude=28.797226,
        longitude=77.133136,
        station_name="Alipur DPCC",
        start_date=datetime(2019, 10, 25),
        end_date=datetime(2019, 10, 25, 23, 59, 59),
    )

    results = find_aqi_anomalies(records)

    assert len(results) == len(records)
    assert all(result.baseline_mean > 0 for result in results)