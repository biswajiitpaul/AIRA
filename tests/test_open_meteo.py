from unittest.mock import patch

from src.adapters.open_meteo import get_weather


def test_get_weather():
    mock_response = {
        "latitude": 25.57,
        "longitude": 91.88,
        "current": {
            "temperature_2m": 25.0,
            "relative_humidity_2m": 70,
            "wind_speed_10m": 8.5,
        },
    }

    with patch("src.adapters.open_meteo.requests.get") as mock_get:
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.raise_for_status.return_value = None

        data = get_weather(25.57, 91.88)

    assert "latitude" in data
    assert "longitude" in data
    assert "current" in data
    assert "temperature_2m" in data["current"]
    assert "relative_humidity_2m" in data["current"]
    assert "wind_speed_10m" in data["current"]