from __future__ import annotations

import numpy as np
import tensorflow as tf

from src.machine_learning.metrics import classification_metrics


def create_autoencoder(
    input_dim: int,
) -> tf.keras.Model:
    """
    Create a feed-forward autoencoder.

    Architecture:

        Input
          ↓
        Encoder
          ↓
       Latent
          ↓
        Decoder
          ↓
        Output
    """

    model = tf.keras.Sequential(
        [
            tf.keras.layers.Input(shape=(input_dim,)),
            tf.keras.layers.Dense(32, activation="relu"),
            tf.keras.layers.Dense(16, activation="relu"),
            tf.keras.layers.Dense(8, activation="relu"),
            tf.keras.layers.Dense(16, activation="relu"),
            tf.keras.layers.Dense(32, activation="relu"),
            tf.keras.layers.Dense(input_dim, activation="linear"),
        ]
    )

    model.compile(
        optimizer="adam",
        loss="mse",
    )

    return model


def calculate_reconstruction_error(
    model,
    X,
    batch_size=10_000,
):
    """
    Calculate Autoencoder reconstruction error in batches.

    Processing in batches prevents the full dataset from being
    loaded into memory during reconstruction-error calculation.
    """
    errors = []

    for start in range(0, len(X), batch_size):
        end = min(start + batch_size, len(X))

        X_batch = X[start:end]

        reconstructed_batch = model.predict(
            X_batch,
            batch_size=batch_size,
            verbose=0,
        )

        batch_errors = np.mean(
            np.square(X_batch - reconstructed_batch),
            axis=1,
        )

        errors.append(batch_errors)

    return np.concatenate(errors)


def determine_threshold(
    reconstruction_errors: np.ndarray,
    percentile: float = 99,
) -> float:
    """
    Determine the anomaly threshold from reconstruction errors.
    """
    return float(
        np.percentile(
            reconstruction_errors,
            percentile,
        )
    )


def predict_anomalies(
    reconstruction_errors: np.ndarray,
    threshold: float,
) -> np.ndarray:
    """
    Mark transactions above the reconstruction-error
    threshold as anomalies.
    """
    return (
        reconstruction_errors > threshold
    ).astype(int)


def evaluate_autoencoder(
    y_true,
    y_pred,
    reconstruction_errors,
) -> dict:
    """
    Evaluate autoencoder anomaly detection.

    Reconstruction error is used as the continuous score so that
    ROC-AUC measures how well the error separates classes.
    """
    return classification_metrics(
        y_true,
        y_pred,
        reconstruction_errors,
        include_accuracy=False,
    )
