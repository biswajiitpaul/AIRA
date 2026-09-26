def persistence_forecast(
    features: list[list[float]],
) -> list[float]:
    """
    Predict the next AQI using the most recent observed AQI.
    """
    return [sample[2] for sample in features]