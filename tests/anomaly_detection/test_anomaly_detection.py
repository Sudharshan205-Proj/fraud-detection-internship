import numpy as np
import pandas as pd
import pytest

from src.anomaly_detection.autoencoder import (
    create_autoencoder,
    determine_threshold,
    predict_anomalies,
)
from src.anomaly_detection.isolation_forest import (
    convert_predictions_to_binary,
    create_isolation_forest,
)
from src.anomaly_detection.pipeline import (
    prepare_features,
    run_autoencoder,
    run_isolation_forest,
    split_and_scale,
)
from tests.helpers import make_processed_frame


def test_isolation_forest_creation():
    model = create_isolation_forest()

    assert model is not None
    assert model.n_estimators == 200


def test_isolation_forest_prediction_conversion():
    predictions = np.array([1, -1, 1, -1])

    converted = convert_predictions_to_binary(
        predictions
    )

    assert converted.tolist() == [
        0,
        1,
        0,
        1,
    ]


def test_autoencoder_creation():
    model = create_autoencoder(10)

    assert model is not None
    assert model.input_shape == (None, 10)
    assert model.output_shape == (None, 10)


def test_autoencoder_threshold():
    errors = np.array(
        [0.1, 0.2, 0.3, 0.4, 10.0]
    )

    threshold = determine_threshold(
        errors,
        percentile=80,
    )

    assert threshold > 0


def test_autoencoder_prediction():
    errors = np.array(
        [0.1, 0.2, 0.3, 5.0]
    )

    predictions = predict_anomalies(
        errors,
        threshold=1.0,
    )

    assert predictions.tolist() == [
        0,
        0,
        0,
        1,
    ]


def test_prepare_features():
    df = pd.DataFrame(
        {
            "step": [1, 2, 3, 4],
            "type": [
                "PAYMENT",
                "TRANSFER",
                "PAYMENT",
                "CASH_OUT",
            ],
            "amount": [
                100,
                200,
                300,
                400,
            ],
            "isFraud": [
                0,
                1,
                0,
                1,
            ],
        }
    )

    X, y = prepare_features(df)

    # Feature matrix is a single float64 NumPy array (target excluded);
    # step + amount + three one-hot transaction types.
    assert isinstance(X, np.ndarray)
    assert X.shape == (4, 5)
    assert len(y) == 4
    assert y.sum() == 2


@pytest.fixture
def synthetic_processed_frame():
    # 120 rows -> 12 fraudulent, enough for a stratified split that keeps
    # both classes in the small test set.
    return make_processed_frame(120)


@pytest.fixture
def scaled_anomaly_splits(synthetic_processed_frame):
    X, y = prepare_features(synthetic_processed_frame)

    assert X.ndim == 2
    assert X.shape[0] == 120
    assert len(y) == 120

    (
        X_train,
        X_test,
        y_train,
        y_test,
        _scaler,
    ) = split_and_scale(X, y)

    assert X_train.shape[1] == X.shape[1]
    assert X_test.shape[1] == X.shape[1]
    assert y_train.nunique() == 2
    assert y_test.nunique() == 2

    return X_train, X_test, y_train, y_test


def _assert_metric_contract(metrics: dict) -> None:
    assert set(metrics) == {
        "precision",
        "recall",
        "f1_score",
        "roc_auc",
    }

    for value in metrics.values():
        assert np.isfinite(value)
        assert 0.0 <= value <= 1.0


def test_isolation_forest_pipeline_end_to_end(scaled_anomaly_splits):
    X_train, X_test, _, y_test = scaled_anomaly_splits

    model, predictions, anomaly_scores, metrics = run_isolation_forest(
        X_train,
        X_test,
        y_test,
    )

    assert model is not None
    assert predictions.shape == (len(y_test),)
    assert anomaly_scores.shape == (len(y_test),)
    assert set(np.unique(predictions)).issubset({0, 1})
    assert np.isfinite(anomaly_scores).all()

    _assert_metric_contract(metrics)


def test_autoencoder_pipeline_end_to_end(scaled_anomaly_splits):
    X_train, X_test, y_train, y_test = scaled_anomaly_splits

    (
        model,
        predictions,
        reconstruction_errors,
        threshold,
        metrics,
    ) = run_autoencoder(
        X_train,
        X_test,
        y_train,
        y_test,
        verbose=0,
    )

    assert model is not None
    assert predictions.shape == (len(y_test),)
    assert reconstruction_errors.shape == (len(y_test),)
    assert set(np.unique(predictions)).issubset({0, 1})
    assert np.isfinite(reconstruction_errors).all()
    assert np.isfinite(threshold)
    assert threshold > 0

    _assert_metric_contract(metrics)
