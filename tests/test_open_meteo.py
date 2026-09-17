from src.adapters.open_meteo import get_weather


def test_get_weather():
    data = get_weather(25.57, 91.88)

    assert "latitude" in data
    assert "longitude" in data
    assert "current" in data
    assert "temperature_2m" in data["current"]
    assert "relative_humidity_2m" in data["current"]
    assert "wind_speed_10m" in data["current"]