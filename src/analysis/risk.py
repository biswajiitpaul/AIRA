from dataclasses import dataclass


@dataclass
class RiskResult:
    risk_score: float
    risk_level: str
    reasons: list[str]


def calculate_risk_score(
    aqi: float,
    anomaly_score: float,
    fire_signal: bool = False,
    wind_speed_kmh: float | None = None,
) -> RiskResult:
    """
    Calculate an explainable environmental risk score.

    This is a prototype scoring model, not an emergency-grade
    prediction system.
    """

    score = 0.0
    reasons = []

    # AQI contribution
    if aqi >= 300:
        score += 50
        reasons.append("Very high AQI")
    elif aqi >= 200:
        score += 40
        reasons.append("High AQI")
    elif aqi >= 150:
        score += 30
        reasons.append("Elevated AQI")
    elif aqi >= 100:
        score += 20
        reasons.append("Moderate AQI")
    elif aqi >= 50:
        score += 10
        reasons.append("Low-to-moderate AQI")

    # Anomaly contribution
    if abs(anomaly_score) >= 3:
        score += 30
        reasons.append("Strong AQI anomaly")
    elif abs(anomaly_score) >= 2:
        score += 20
        reasons.append("AQI anomaly detected")

    # Fire signal
    if fire_signal:
        score += 15
        reasons.append("Nearby fire activity detected")

    # Low wind can be associated with pollutant accumulation.
    if wind_speed_kmh is not None and wind_speed_kmh < 5:
        score += 5
        reasons.append("Low wind conditions")

    score = min(score, 100)

    if score >= 70:
        risk_level = "HIGH"
    elif score >= 40:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return RiskResult(
        risk_score=score,
        risk_level=risk_level,
        reasons=reasons,
    )
def detect_hotspot(
    risk_results: list[RiskResult],
    minimum_high_risk: int = 2,
) -> bool:
    """
    Determine whether a location shows repeated high-risk conditions.

    This is a prototype hotspot rule, not an emergency-grade detector.
    """

    high_risk_count = sum(
        result.risk_level == "HIGH"
        for result in risk_results
    )

    return high_risk_count >= minimum_high_risk