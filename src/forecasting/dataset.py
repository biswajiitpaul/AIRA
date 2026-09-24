from typing import List, Tuple

from src.models.air_quality import NormalizedAirQuality


def create_forecasting_dataset(
    records: List[NormalizedAirQuality],
    lookback: int = 3,
) -> Tuple[List[List[float]], List[float]]:
    """
    Convert ordered AQI observations into supervised forecasting samples.

    Each sample uses the previous `lookback` AQI values to predict
    the next hourly AQI value.

    Example with lookback=3:

        [100, 110, 120] -> 130
        [110, 120, 130] -> 140

    The records should already be ordered chronologically.
    """

    if lookback < 1:
        raise ValueError("lookback must be at least 1")

    if len(records) <= lookback:
        return [], []

    values = [record.value for record in records]

    features = []
    targets = []

    for index in range(lookback, len(values)):
        features.append(values[index - lookback:index])
        targets.append(values[index])

    return features, targets
def split_time_series(
    features: list[list[float]],
    targets: list[float],
    train_ratio: float = 0.8,
) -> tuple[
    list[list[float]],
    list[list[float]],
    list[float],
    list[float],
]:
    """
    Split forecasting samples chronologically.

    Earlier samples are used for training and later samples
    are used for testing.
    """

    if len(features) != len(targets):
        raise ValueError("features and targets must have the same length")

    if not 0 < train_ratio < 1:
        raise ValueError("train_ratio must be between 0 and 1")

    split_index = int(len(features) * train_ratio)

    train_features = features[:split_index]
    test_features = features[split_index:]

    train_targets = targets[:split_index]
    test_targets = targets[split_index:]

    return (
        train_features,
        test_features,
        train_targets,
        test_targets,
    )