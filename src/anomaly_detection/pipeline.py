from __future__ import annotations

import argparse

import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

RANDOM_STATE = 42

np.random.seed(RANDOM_STATE)
tf.random.set_seed(RANDOM_STATE)

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
from src.data_processing.process_data import load_processed_dataset

TARGET_COLUMN = "isFraud"


def prepare_features(
    df: pd.DataFrame,
):
    """
    Prepare numerical features for anomaly detection.

    The processed dataset contains engineered numerical features plus
    the categorical ``type`` variable, which is one-hot encoded. All
    numeric columns are combined into a single float64 feature matrix
    with ``inf``/``NaN`` replaced in place, so the original frame is
    not duplicated.
    """

    if TARGET_COLUMN not in df.columns:
        raise ValueError(
            f"Missing target column: {TARGET_COLUMN}"
        )

    y = df[TARGET_COLUMN].astype(int)

    X = df.drop(
        columns=[TARGET_COLUMN]
    )

    if "type" in X.columns:
        X = pd.get_dummies(
            X,
            columns=["type"],
            dtype=int,
        )

    numeric_columns = X.select_dtypes(include="number").columns

    if len(numeric_columns) < len(X.columns):
        X = X[numeric_columns]

    # Replace infinities and NaN in a single allocation, then build one
    # float64 matrix that the scaler and models reuse.
    X = np.nan_to_num(
        X.to_numpy(dtype=np.float64),
        nan=0.0,
        posinf=0.0,
        neginf=0.0,
    )

    return X, y


def split_and_scale(
    X: np.ndarray,
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
        contamination=0.0013,
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
    verbose: int = 1,
):
    """
    Train and evaluate the autoencoder.

    The autoencoder learns normal transaction behaviour
    by training only on legitimate transactions.

    Parameters
    ----------
    verbose:
        Keras training verbosity (0 silences per-epoch output).
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
        verbose=verbose,
    )

    training_errors = calculate_reconstruction_error(
        model,
        X_train_normal,
    )

    threshold = determine_threshold(
        training_errors,
        percentile=99,
    )

    # Free the training reconstruction errors and normal-only slice;
    # only the model and threshold are needed from here on.
    del training_errors, X_train_normal

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


def main(max_rows: int | None = None) -> None:
    """
    Run the complete anomaly-detection workflow.
    """

    print("Loading processed PaySim dataset...")

    df = load_processed_dataset(max_rows=max_rows)

    if max_rows is not None:
        print(f"Sample mode active: using at most {max_rows:,} rows.")

    print(f"Dataset shape: {df.shape}")

    X, y = prepare_features(df)

    # The NumPy feature matrix is now the only thing the pipeline needs.
    del df

    print(f"Feature matrix shape: {X.shape}")

    (
        X_train,
        X_test,
        y_train,
        y_test,
        _scaler,
    ) = split_and_scale(
        X,
        y,
    )
    del X

    print("\nRunning Isolation Forest...")

    (
        _isolation_model,
        _isolation_predictions,
        _isolation_scores,
        isolation_metrics,
    ) = run_isolation_forest(
        X_train,
        X_test,
        y_test,
    )

    print("\nIsolation Forest Results")

    for metric, value in isolation_metrics.items():
        print(f"{metric}: {value:.6f}")

    print("\nRunning Autoencoder...")

    (
        _autoencoder_model,
        _autoencoder_predictions,
        _reconstruction_errors,
        threshold,
        autoencoder_metrics,
    ) = run_autoencoder(
        X_train,
        X_test,
        y_train,
        y_test,
    )

    print("\nAutoencoder Results")

    for metric, value in autoencoder_metrics.items():
        print(f"{metric}: {value:.6f}")

    print(f"\nAutoencoder threshold: {threshold:.6f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Run the Isolation Forest and autoencoder anomaly-detection "
            "workflow on the processed PaySim dataset."
        ),
    )
    parser.add_argument(
        "--max-rows",
        type=int,
        default=None,
        metavar="N",
        help="Optional row cap for fast sample-mode runs (default: full dataset).",
    )
    args = parser.parse_args()

    main(max_rows=args.max_rows)
