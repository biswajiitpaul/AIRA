from src.forecasting.baseline import persistence_forecast


def test_persistence_forecast():
    features = [
        [100, 110, 120],
        [110, 120, 130],
        [120, 130, 140],
    ]

    predictions = persistence_forecast(features)

    assert predictions == [120, 130, 140]