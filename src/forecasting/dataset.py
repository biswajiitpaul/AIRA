from typing import List, Tuple

from src.models.air_quality import NormalizedAirQuality


def create_forecasting_dataset(
    records: List[NormalizedAirQuality],
    lookback: int = 3,
) -> Tuple[List[List[float]], List[float]]:
    """
    Convert ordered AQI observations into supervised forecasting samples.

    Each sample uses the previous `lookback` AQI values plus
    time-based features to predict the next AQI value.

    Features:
        - previous AQI values
        - target hour
        - target day of week

    The records should already be ordered chronologically.
    """

    if lookback < 1:
        raise ValueError("lookback must be at least 1")

    if len(records) <= lookback:
        return [], []

    features = []
    targets = []

    for index in range(lookback, len(records)):
        previous_values = [
            record.value
            for record in records[index - lookback:index]
        ]

        target_record = records[index]

        hour = target_record.timestamp.hour
        day_of_week = target_record.timestamp.weekday()

        sample = previous_values + [
            float(hour),
            float(day_of_week),
        ]

        features.append(sample)
        targets.append(target_record.value)

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