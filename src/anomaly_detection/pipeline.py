from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from src.anomaly_detection.autoencoder import (
    calculate_reconstruction_error,
    create_autoencoder,
    determine_threshold,
    evaluate_autoencoder,
)
from src.anomaly_detection.autoencoder import (
    predict_anomalies as autoencoder_predict,
)
from src.anomaly_detection.isolation_forest import (
    convert_predictions_to_binary,
    create_isolation_forest,
    evaluate_isolation_forest,
    fit_isolation_forest,
)
from src.anomaly_detection.isolation_forest import (
    predict_anomalies as isolation_predict,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "paysim_processed.csv"
)


TARGET_COLUMN = "isFraud"


def load_dataset() -> pd.DataFrame:
    """
    Load the processed PaySim dataset.
    """
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}"
        )

    return pd.read_csv(DATA_PATH)


def prepare_features(
    df: pd.DataFrame,
):
    """
    Prepare numerical features for anomaly detection.

    The processed dataset already contains engineered
    numerical features, while 'type' is categorical.

    One-hot encoding is applied to 'type'.
    """

    if TARGET_COLUMN not in df.columns:
        raise ValueError(
            f"Missing target column: {TARGET_COLUMN}"
        )

    data = df.copy()

    y = data[TARGET_COLUMN].astype(int)

    X = data.drop(
        columns=[TARGET_COLUMN]
    )

    if "type" in X.columns:
        X = pd.get_dummies(
            X,
            columns=["type"],
            dtype=int,
        )

    X = X.replace(
        [np.inf, -np.inf],
        np.nan,
    )

    X = X.fillna(0)

    return X, y


def split_and_scale(
    X,
    y,
):
    """
    Split the dataset and standardize numerical features.
    """

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(
        X_train
    )

    X_test_scaled = scaler.transform(
        X_test
    )

    return (
        X_train_scaled,
        X_test_scaled,
        y_train,
        y_test,
        scaler,
    )


def run_isolation_forest(
    X_train,
    X_test,
    y_test,
):
    """
    Train and evaluate Isolation Forest.
    """

    model = create_isolation_forest(
        contamination=0.01,
        random_state=42,
    )

    fit_isolation_forest(
        model,
        X_train,
    )

    raw_predictions, anomaly_scores = (
        isolation_predict(
            model,
            X_test,
        )
    )

    predictions = convert_predictions_to_binary(
        raw_predictions
    )

    metrics = evaluate_isolation_forest(
        y_test,
        predictions,
        anomaly_scores,
    )

    return model, predictions, anomaly_scores, metrics


def run_autoencoder(
    X_train,
    X_test,
    y_train,
    y_test,
):
    """
    Train and evaluate the autoencoder.

    The autoencoder learns normal transaction behaviour
    by training only on legitimate transactions.
    """

    normal_training_mask = (
        y_train.to_numpy() == 0
    )

    X_train_normal = X_train[
        normal_training_mask
    ]

    model = create_autoencoder(
        X_train.shape[1]
    )

    model.fit(
        X_train_normal,
        X_train_normal,
        epochs=10,
        batch_size=256,
        validation_split=0.1,
        shuffle=True,
        verbose=1,
    )

    training_errors = calculate_reconstruction_error(
        model,
        X_train_normal,
    )

    threshold = determine_threshold(
        training_errors,
        percentile=99,
    )

    test_errors = calculate_reconstruction_error(
        model,
        X_test,
    )

    predictions = autoencoder_predict(
        test_errors,
        threshold,
    )

    metrics = evaluate_autoencoder(
        y_test,
        predictions,
        test_errors,
    )

    return (
        model,
        predictions,
        test_errors,
        threshold,
        metrics,
    )


def main():
    """
    Run the complete anomaly-detection workflow.
    """

    print("Loading processed PaySim dataset...")

    df = load_dataset()

    print(
        f"Dataset shape: {df.shape}"
    )

    X, y = prepare_features(df)

    print(
        f"Feature matrix shape: {X.shape}"
    )

    (
        X_train,
        X_test,
        y_train,
        y_test,
        scaler,  # noqa: RUF059
    ) = split_and_scale(
        X,
        y,
    )

    print(
        "\nRunning Isolation Forest..."
    )

    (
        isolation_model,  # noqa: RUF059
        isolation_predictions,  # noqa: RUF059
        isolation_scores,  # noqa: RUF059
        isolation_metrics,
    ) = run_isolation_forest(
        X_train,
        X_test,
        y_test,
    )

    print(
        "\nIsolation Forest Results"
    )

    for metric, value in isolation_metrics.items():
        print(
            f"{metric}: {value:.6f}"
        )

    print(
        "\nRunning Autoencoder..."
    )

    (
        autoencoder_model,  # noqa: RUF059
        autoencoder_predictions,  # noqa: RUF059
        reconstruction_errors,  # noqa: RUF059
        threshold,
        autoencoder_metrics,
            ) = run_autoencoder(
        X_train,
        X_test,
        y_train,
        y_test,
    )

    print(
        "\nAutoencoder Results"
    )

    for metric, value in autoencoder_metrics.items():
        print(
            f"{metric}: {value:.6f}"
        )

    print(
        f"\nAutoencoder threshold: {threshold:.6f}"
    )


if __name__ == "__main__":
    main()
