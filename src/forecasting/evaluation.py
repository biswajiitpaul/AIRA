from math import sqrt

from sklearn.metrics import mean_absolute_error, mean_squared_error


def evaluate_forecast(
    actual: list[float],
    predicted: list[float],
) -> dict[str, float]:
    """
    Evaluate AQI forecasts using MAE and RMSE.
    """
    if len(actual) != len(predicted):
        raise ValueError("actual and predicted must have the same length")

    mae = mean_absolute_error(actual, predicted)
    rmse = sqrt(mean_squared_error(actual, predicted))

    return {
        "mae": float(mae),
        "rmse": float(rmse),
    }