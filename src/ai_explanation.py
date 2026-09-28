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

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return (
            f"AIRA classified this situation as {risk_level} risk "
            f"with a score of {risk_score:.1f}. "
            f"Detected signals: {', '.join(reasons)}. "
            "AI explanation is unavailable because the API key is not set."
        )

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

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
        )
        return response.text
    except Exception as exc:
        print(f"Gemini unavailable: {exc}")
        return (
            f"AIRA classified this situation as {risk_level} risk "
            f"with a score of {risk_score:.1f}. "
            f"Detected signals: {', '.join(reasons)}. "
            "AI explanation is temporarily unavailable."
        )


def explain_risk_result(aqi: float, risk_result: RiskResult) -> str:
    return explain_environmental_risk(
        aqi=aqi,
        risk_level=risk_result.risk_level,
        risk_score=risk_result.risk_score,
        reasons=risk_result.reasons,
    )
