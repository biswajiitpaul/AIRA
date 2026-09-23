from src.analysis.risk import calculate_risk_score


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