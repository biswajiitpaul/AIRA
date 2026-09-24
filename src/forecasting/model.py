from sklearn.linear_model import LinearRegression


def train_linear_forecaster(
    train_features: list[list[float]],
    train_targets: list[float],
) -> LinearRegression:
    """
    Train a simple linear regression model
    for next-hour AQI forecasting.
    """
    model = LinearRegression()
    model.fit(train_features, train_targets)
    return model


def predict_aqi(
    model: LinearRegression,
    features: list[list[float]],
) -> list[float]:
    """
    Generate AQI predictions using the trained model.
    """
    return model.predict(features).tolist()