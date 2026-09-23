from dataclasses import dataclass
from statistics import mean, pstdev
from typing import List


@dataclass
class AnomalyResult:
    current_value: float
    baseline_mean: float
    z_score: float
    is_anomaly: bool
    timestamp: object = None
    station_name: str = ""


def detect_aqi_anomaly(
    current_value: float,
    baseline_values: List[float],
    z_threshold: float = 2.0,
) -> AnomalyResult:
    if not baseline_values:
        raise ValueError("baseline_values cannot be empty")

    baseline_mean = mean(baseline_values)

    if len(baseline_values) == 1:
        z_score = 0.0
    else:
        standard_deviation = pstdev(baseline_values)

        if standard_deviation == 0:
            z_score = 0.0
        else:
            z_score = (current_value - baseline_mean) / standard_deviation

    is_anomaly = abs(z_score) >= z_threshold

    return AnomalyResult(
        current_value=current_value,
        baseline_mean=baseline_mean,
        z_score=z_score,
        is_anomaly=is_anomaly,
    )


def find_aqi_anomalies(
    records: List,
    z_threshold: float = 2.0,
) -> List[AnomalyResult]:
    if len(records) < 2:
        return []

    values = [record.value for record in records]

    results = []

    for index, record in enumerate(records):
        baseline_values = values[:index] + values[index + 1:]

        result = detect_aqi_anomaly(
            current_value=record.value,
            baseline_values=baseline_values,
            z_threshold=z_threshold,
        )

        result.timestamp = record.timestamp
        result.station_name = record.station_name or ""

        results.append(result)

    return results