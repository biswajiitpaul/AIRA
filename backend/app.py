from flask import Flask, jsonify, request

from src.analysis.risk import calculate_risk_score
from src.ai_explanation import explain_risk_result

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "service": "AIRA API"
    })


@app.route("/api/risk", methods=["POST"])
def risk_analysis():
    data = request.get_json()

    if not data:
        return jsonify({"error": "JSON body is required"}), 400

    aqi = data.get("aqi")
    anomaly_score = data.get("anomaly_score", 0)
    fire_signal = data.get("fire_signal", False)
    wind_speed_kmh = data.get("wind_speed_kmh")

    if aqi is None:
        return jsonify({"error": "aqi is required"}), 400

    risk = calculate_risk_score(
        aqi=float(aqi),
        anomaly_score=float(anomaly_score),
        fire_signal=bool(fire_signal),
        wind_speed_kmh=(
            float(wind_speed_kmh)
            if wind_speed_kmh is not None
            else None
        ),
    )

    explanation = explain_risk_result(
        aqi=float(aqi),
        risk_result=risk,
    )

    return jsonify({
        "aqi": float(aqi),
        "risk_score": risk.risk_score,
        "risk_level": risk.risk_level,
        "reasons": risk.reasons,
        "ai_explanation": explanation,
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
