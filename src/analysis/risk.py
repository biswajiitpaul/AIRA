from dataclasses import dataclass
from dataclasses import dataclass
from typing import Optional

@dataclass
class RiskResult:
    risk_score: float
    risk_level: str
    reasons: list[str]

@dataclass
class HotspotResult:
    station_name: str
    latitude: float
    longitude: float
    timestamp: object
    risk_score: float
    risk_level: str
    high_risk_observations: int
    reasons: list[str]
    confidence: str

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
    station_name: str = "Unknown",
    latitude: float = 0.0,
    longitude: float = 0.0,
    timestamp=None,
) -> HotspotResult | None:
    """
    Create structured hotspot intelligence when repeated
    high-risk conditions are detected.

    This is a prototype rule, not an emergency-grade detector.
    """

    high_risk_results = [
        result
        for result in risk_results
        if result.risk_level == "HIGH"
    ]

    high_risk_count = len(high_risk_results)

    if high_risk_count < minimum_high_risk:
        return None

    latest_result = max(
    high_risk_results,
    key=lambda result: result.risk_score,
)

    # Combine unique reasons from high-risk observations.
    reasons = []
    for result in high_risk_results:
        for reason in result.reasons:
            if reason not in reasons:
                reasons.append(reason)

    # Prototype confidence based on repeated high-risk observations.
    if high_risk_count >= 4:
        confidence = "HIGH"
    elif high_risk_count >= 2:
        confidence = "MEDIUM"
    else:
        confidence = "LOW"

    return HotspotResult(
        station_name=station_name,
        latitude=latitude,
        longitude=longitude,
        timestamp=timestamp,
        risk_score=latest_result.risk_score,
        risk_level=latest_result.risk_level,
        high_risk_observations=high_risk_count,
        reasons=reasons,
        confidence=confidence,
    )