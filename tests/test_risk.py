from src.analysis.risk import (calculate_risk_score,detect_hotspot,classify_hotspot_behavior,)


def test_high_risk_score():
    result = calculate_risk_score(
        aqi=355,
        anomaly_score=3.2,
        fire_signal=True,
        wind_speed_kmh=3,
    )

    assert result.risk_score == 100
    assert result.risk_level == "HIGH"
    assert len(result.reasons) >= 3


def test_medium_risk_score():
    result = calculate_risk_score(
        aqi=180,
        anomaly_score=2.1,
        fire_signal=False,
        wind_speed_kmh=10,
    )

    assert result.risk_level == "MEDIUM"
    assert 40 <= result.risk_score < 70


def test_low_risk_score():
    result = calculate_risk_score(
        aqi=40,
        anomaly_score=0.5,
        fire_signal=False,
        wind_speed_kmh=15,
    )

    assert result.risk_level == "LOW"
    assert result.risk_score < 40
from datetime import datetime

from src.adapters.opencity_delhi import parse_opencity_aqi
from src.analysis.anomaly import detect_aqi_anomaly


def test_risk_with_real_opencity_data():
    records = parse_opencity_aqi(
        file_path="fixtures/opencity_alipur_dpcc_2017_2023.csv",
        latitude=28.797226,
        longitude=77.133136,
        station_name="Alipur DPCC",
        start_date=datetime(2019, 10, 25),
        end_date=datetime(2019, 11, 10, 23, 59, 59),
    )

    assert len(records) == 371

    current = records[-1]
    baseline = [record.value for record in records[:-1]]

    anomaly = detect_aqi_anomaly(
        current_value=current.value,
        baseline_values=baseline,
    )

    risk = calculate_risk_score(
        aqi=current.value,
        anomaly_score=anomaly.z_score,
        fire_signal=False,
        wind_speed_kmh=None,
    )

    assert 0 <= risk.risk_score <= 100
    assert risk.risk_level in {"LOW", "MEDIUM", "HIGH"}
    assert len(risk.reasons) >= 1
def test_structured_hotspot_result():
    results = [
        calculate_risk_score(350, 3.0, True, 3),
        calculate_risk_score(320, 2.8, False, 4),
        calculate_risk_score(80, 0.5, False, 15),
    ]

    hotspot = detect_hotspot(
        risk_results=results,
        minimum_high_risk=2,
        station_name="Alipur DPCC",
        latitude=28.797226,
        longitude=77.133136,
        timestamp=None,
    )

    assert hotspot is not None
    assert hotspot.station_name == "Alipur DPCC"
    assert hotspot.latitude == 28.797226
    assert hotspot.longitude == 77.133136
    assert hotspot.high_risk_observations == 2
    assert hotspot.risk_level == "HIGH"
    assert hotspot.confidence == "MEDIUM"
    assert len(hotspot.reasons) >= 1
def test_structured_hotspot_with_real_opencity_data():
    records = parse_opencity_aqi(
        file_path="fixtures/opencity_alipur_dpcc_2017_2023.csv",
        latitude=28.797226,
        longitude=77.133136,
        station_name="Alipur DPCC",
        start_date=datetime(2019, 10, 25),
        end_date=datetime(2019, 10, 25, 23, 59, 59),
    )

    risk_results = []

    for index, record in enumerate(records):
        baseline = [
            item.value
            for item in records
            if item is not record
        ]

        anomaly = detect_aqi_anomaly(
            current_value=record.value,
            baseline_values=baseline,
        )

        risk = calculate_risk_score(
            aqi=record.value,
            anomaly_score=anomaly.z_score,
            fire_signal=False,
            wind_speed_kmh=None,
        )

        risk_results.append(risk)

    hotspot = detect_hotspot(
        risk_results=risk_results,
        minimum_high_risk=2,
        station_name="Alipur DPCC",
        latitude=28.797226,
        longitude=77.133136,
        timestamp=records[-1].timestamp,
    )

    if hotspot is not None:
        assert hotspot.station_name == "Alipur DPCC"
        assert hotspot.latitude == 28.797226
        assert hotspot.longitude == 77.133136
        assert hotspot.high_risk_observations >= 2
        assert hotspot.risk_level == "HIGH"
        assert hotspot.confidence in {"MEDIUM", "HIGH"}
        assert len(hotspot.reasons) >= 1


def test_persistent_hotspot_behavior():
    results = [
        calculate_risk_score(300, 3.0),
        calculate_risk_score(320, 3.1),
        calculate_risk_score(350, 3.2),
    ]

    behavior = classify_hotspot_behavior(results)

    assert behavior == "PERSISTENT"


def test_emerging_hotspot_behavior():
    results = [
        calculate_risk_score(60, 0.5),
        calculate_risk_score(80, 0.8),
        calculate_risk_score(180, 2.2),
        calculate_risk_score(250, 2.8),
    ]

    behavior = classify_hotspot_behavior(results)

    assert behavior == "EMERGING"


def test_transient_hotspot_behavior():
    results = [
        calculate_risk_score(70, 0.5),
        calculate_risk_score(350, 3.5),
        calculate_risk_score(80, 0.5),
    ]

    behavior = classify_hotspot_behavior(results)

    assert behavior == "TRANSIENT"