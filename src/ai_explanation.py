import os

from dotenv import load_dotenv
from google import genai
from src.analysis.risk import RiskResult

load_dotenv()


def explain_environmental_risk(
    aqi: float,
    risk_level: str,
    risk_score: float,
    reasons: list[str],
) -> str:
    """
    Generate a plain-language explanation of AIRA's
    already-computed environmental risk signals.
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set")

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are AIRA, an environmental intelligence assistant.

Explain the environmental risk using ONLY the structured
evidence provided below.

AQI: {aqi}
Risk level: {risk_level}
Risk score: {risk_score}
Detected signals:
{chr(10).join(f"- {reason}" for reason in reasons)}

Requirements:
- Explain why AIRA classified the situation this way.
- Use simple language.
- Do not invent measurements, causes, locations, or events.
- Do not claim certainty about pollution sources.
- Clearly distinguish detected signals from possible explanations.
- Keep the response under 120 words.
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
    )

    return response.text
def explain_risk_result(aqi: float, risk_result: RiskResult) -> str:
    """
    Generate a Gemini explanation directly from AIRA's
    structured risk result.
    """
    return explain_environmental_risk(
        aqi=aqi,
        risk_level=risk_result.risk_level,
        risk_score=risk_result.risk_score,
        reasons=risk_result.reasons,
    )
