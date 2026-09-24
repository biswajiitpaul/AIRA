from datetime import datetime
from src.forecasting.baseline import persistence_forecast

from src.adapters.opencity_delhi import parse_opencity_aqi
from src.forecasting.dataset import (
    create_forecasting_dataset,
    split_time_series,
)
from src.forecasting.model import train_linear_forecaster, predict_aqi
from src.forecasting.evaluation import evaluate_forecast


# Load real Alipur DPCC AQI data
records = parse_opencity_aqi(
    file_path="fixtures/opencity_alipur_dpcc_2017_2023.csv",
    latitude=28.797226,
    longitude=77.133136,
    station_name="Alipur DPCC",
    start_date=datetime(2019, 10, 25),
    end_date=datetime(2019, 11, 10, 23, 59, 59),
)

# Create forecasting samples
features, targets = create_forecasting_dataset(
    records,
    lookback=3,
)

# Chronological train/test split
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

# Train model
model = train_linear_forecaster(
    train_features,
    train_targets,
)

# Generate Linear Regression predictions
predictions = predict_aqi(
    model,
    test_features,
)

# Generate persistence baseline predictions
baseline_predictions = persistence_forecast(
    test_features,
)

# Evaluate Linear Regression
metrics = evaluate_forecast(
    test_targets,
    predictions,
)

# Evaluate persistence baseline
baseline_metrics = evaluate_forecast(
    test_targets,
    baseline_predictions,
)

print("AIRA AQI FORECASTING")
print("--------------------")
print(f"Total observations: {len(records)}")
print(f"Training samples: {len(train_features)}")
print(f"Testing samples: {len(test_features)}")
print("\nLinear Regression")
print(f"MAE: {metrics['mae']:.2f}")
print(f"RMSE: {metrics['rmse']:.2f}")

print("\nPersistence Baseline")
print(f"MAE: {baseline_metrics['mae']:.2f}")
print(f"RMSE: {baseline_metrics['rmse']:.2f}")

print("\nSample predictions:")
for actual, predicted in zip(test_targets[:5], predictions[:5]):
    print(
        f"Actual AQI: {actual:.2f} | "
        f"Predicted AQI: {predicted:.2f}"
    )