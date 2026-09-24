from datetime import datetime, timedelta
from src.forecasting.dataset import (
    create_forecasting_dataset,
    split_time_series,
)


from src.models.air_quality import NormalizedAirQuality


def create_test_records(values):
    start_time = datetime(2019, 10, 25, 0, 0)

    return [
        NormalizedAirQuality(
            latitude=28.797226,
            longitude=77.133136,
            timestamp=start_time + timedelta(hours=index),
            value=value,
            parameter="AQI",
            unit="index",
            station_name="Alipur DPCC",
            source="CPCB/OpenCity",
        )
        for index, value in enumerate(values)
    ]


def test_create_forecasting_dataset():
    records = create_test_records(
        [100, 110, 120, 130, 140]
    )

    features, targets = create_forecasting_dataset(
        records,
        lookback=3,
    )

    assert features == [
        [100, 110, 120],
        [110, 120, 130],
    ]

    assert targets == [130, 140]


def test_forecasting_dataset_with_small_input():
    records = create_test_records([100, 110, 120])

    features, targets = create_forecasting_dataset(
        records,
        lookback=3,
    )

    assert features == []
    assert targets == []


def test_invalid_lookback():
    records = create_test_records([100, 110, 120])

    try:
        create_forecasting_dataset(
            records,
            lookback=0,
        )
        assert False
    except ValueError as error:
        assert str(error) == "lookback must be at least 1"

from datetime import datetime

from src.adapters.opencity_delhi import parse_opencity_aqi


def test_forecasting_dataset_with_real_opencity_data():
    records = parse_opencity_aqi(
        file_path="fixtures/opencity_alipur_dpcc_2017_2023.csv",
        latitude=28.797226,
        longitude=77.133136,
        station_name="Alipur DPCC",
        start_date=datetime(2019, 10, 25),
        end_date=datetime(2019, 11, 10, 23, 59, 59),
    )

    features, targets = create_forecasting_dataset(
        records,
        lookback=3,
    )

    assert len(records) == 371
    assert len(features) == 368
    assert len(targets) == 368
    assert len(features[0]) == 3
    assert features[0] == [
        records[0].value,
        records[1].value,
        records[2].value,
    ]
    assert targets[0] == records[3].value


def test_split_time_series():
    features = [
        [1, 2, 3],
        [2, 3, 4],
        [3, 4, 5],
        [4, 5, 6],
        [5, 6, 7],
    ]

    targets = [4, 5, 6, 7, 8]

    (
        train_features,
        test_features,
        train_targets,
        test_targets,
    ) = split_time_series(
        features,
        targets,
        train_ratio=0.8,
    )

    assert train_features == [
        [1, 2, 3],
        [2, 3, 4],
        [3, 4, 5],
        [4, 5, 6],
    ]

    assert test_features == [[5, 6, 7]]

    assert train_targets == [4, 5, 6, 7]
    assert test_targets == [8]


def test_invalid_train_ratio():
    features = [[1, 2, 3]]
    targets = [4]

    try:
        split_time_series(
            features,
            targets,
            train_ratio=1.0,
        )
        assert False
    except ValueError as error:
        assert str(error) == "train_ratio must be between 0 and 1"