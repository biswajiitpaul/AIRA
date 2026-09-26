from src.analysis.risk import calculate_risk_score
from src.ai_explanation import explain_risk_result
import src.ai_explanation as ai_explanation


class FakeResponse:
    text = "AIRA detected high environmental risk based on the provided signals."


class FakeModels:
    def generate_content(self, model, contents):
        return FakeResponse()


class FakeClient:
    def __init__(self, api_key):
        self.models = FakeModels()


def test_explain_risk_result(monkeypatch):
    monkeypatch.setattr(ai_explanation.genai, "Client", FakeClient)

    risk = calculate_risk_score(
        aqi=335,
        anomaly_score=3.2,
        wind_speed_kmh=3,
    )

    explanation = explain_risk_result(335, risk)

    assert explanation == (
        "AIRA detected high environmental risk based on "
        "the provided signals."
    )
