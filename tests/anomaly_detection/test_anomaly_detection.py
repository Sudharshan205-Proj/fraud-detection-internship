import numpy as np
import pandas as pd

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
)


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

    assert "isFraud" not in X.columns
    assert len(X) == 4
    assert len(y) == 4
    assert y.sum() == 2
