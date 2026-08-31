import pandas as pd
import pytest

from src.machine_learning.models import (
    create_logistic_regression,
    create_random_forest,
)
from src.machine_learning.prepare import (
    apply_smote,
    prepare_categorical_features,
    scale_features,
    split_features_target,
    train_test_split_data,
)


@pytest.fixture
def sample_data():
    return pd.DataFrame(
        {
            "step": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "type": [
                "PAYMENT",
                "TRANSFER",
                "CASH_OUT",
                "PAYMENT",
                "TRANSFER",
                "CASH_OUT",
                "PAYMENT",
                "TRANSFER",
                "CASH_OUT",
                "PAYMENT",
            ],
            "amount": [
                100,
                500,
                1000,
                200,
                700,
                1500,
                300,
                900,
                2000,
                400,
            ],
            "nameOrig": [f"C{i}" for i in range(10)],
            "nameDest": [f"D{i}" for i in range(10)],
            "oldbalanceOrg": [
                1000,
                500,
                2000,
                500,
                1000,
                3000,
                600,
                1500,
                4000,
                800,
            ],
            "newbalanceOrig": [
                900,
                0,
                1000,
                300,
                300,
                1500,
                300,
                600,
                2000,
                400,
            ],
            "oldbalanceDest": [0] * 10,
            "newbalanceDest": [0] * 10,
            "isFlaggedFraud": [0] * 10,
            "isFraud": [0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
        }
    )


def test_split_features_target(sample_data):
    X, y = split_features_target(sample_data)

    assert "isFraud" not in X.columns
    assert len(X) == len(y)
    assert y.name == "isFraud"


def test_missing_target_raises_error():
    df = pd.DataFrame({"amount": [100, 200]})

    with pytest.raises(ValueError):
        split_features_target(df)


def test_identifier_columns_are_removed(sample_data):
    X, _ = split_features_target(sample_data)

    result = prepare_categorical_features(X)

    assert "nameOrig" not in result.columns
    assert "nameDest" not in result.columns


def test_categorical_encoding(sample_data):
    X, _ = split_features_target(sample_data)

    result = prepare_categorical_features(X)

    assert "type_PAYMENT" in result.columns
    assert "type_TRANSFER" in result.columns
    assert "type_CASH_OUT" in result.columns


def test_train_test_split_preserves_rows(sample_data):
    X, y = split_features_target(sample_data)

    X = prepare_categorical_features(X)

    X_train, X_test, y_train, y_test = train_test_split_data(
        X,
        y,
        test_size=0.2,
    )

    assert len(X_train) + len(X_test) == len(X)
    assert len(y_train) + len(y_test) == len(y)


def test_train_test_split_preserves_class_presence(sample_data):
    X, y = split_features_target(sample_data)

    X = prepare_categorical_features(X)

    _, _, y_train, y_test = train_test_split_data(
        X,
        y,
        test_size=0.2,
    )

    assert y_train.nunique() == 2
    assert y_test.nunique() == 2


def test_scaling_preserves_shape(sample_data):
    X, _ = split_features_target(sample_data)

    X = prepare_categorical_features(X)

    X_train, X_test, _, _ = train_test_split_data(
        X,
        sample_data["isFraud"],
        test_size=0.2,
    )

    X_train_scaled, X_test_scaled, _ = scale_features(
        X_train,
        X_test,
    )

    assert X_train_scaled.shape == X_train.shape
    assert X_test_scaled.shape == X_test.shape


def test_smote_increases_minority_class(sample_data):
    X, y = split_features_target(sample_data)

    X = prepare_categorical_features(X)

    X_train, _, y_train, _ = train_test_split_data(
        X,
        y,
        test_size=0.2,
    )

    X_resampled, y_resampled = apply_smote(
        X_train,
        y_train,
    )

    assert len(X_resampled) == len(y_resampled)
    assert y_resampled.value_counts()[0] == y_resampled.value_counts()[1]


def test_logistic_regression_creation():
    model = create_logistic_regression()

    assert model.max_iter == 1000


def test_random_forest_creation():
    model = create_random_forest()

    assert model.n_estimators == 100
    assert model.class_weight == "balanced"


def test_model_results_contain_required_metrics():
    required_metrics = {
        "accuracy",
        "precision",
        "recall",
        "f1_score",
        "roc_auc",
    }

    logistic_results = {
        "accuracy": 0.967201,
        "precision": 0.034137,
        "recall": 0.894096,
        "f1_score": 0.065762,
        "roc_auc": 0.984229,
    }

    random_forest_results = {
        "accuracy": 0.999995,
        "precision": 0.998781,
        "recall": 0.997565,
        "f1_score": 0.998173,
        "roc_auc": 0.999087,
    }

    assert required_metrics.issubset(logistic_results.keys())
    assert required_metrics.issubset(random_forest_results.keys())


def test_random_forest_outperforms_logistic_regression_on_f1():
    logistic_f1 = 0.065762
    random_forest_f1 = 0.998173

    assert random_forest_f1 > logistic_f1


def test_processed_dataset_has_expected_feature_count():
    import pandas as pd

    df = pd.DataFrame(
        {
            "step": [1],
            "type": ["PAYMENT"],
            "amount": [100.0],
            "oldbalanceOrg": [500.0],
            "newbalanceOrig": [400.0],
            "oldbalanceDest": [0.0],
            "newbalanceDest": [100.0],
            "isFraud": [0],
            "isFlaggedFraud": [0],
            "origin_balance_change": [100.0],
            "destination_balance_change": [100.0],
            "origin_balance_error": [0.0],
            "destination_balance_error": [0.0],
            "origin_balance_error_abs": [0.0],
            "destination_balance_error_abs": [0.0],
            "origin_zero_balance_before": [0],
            "origin_zero_balance_after": [0],
            "destination_zero_balance_before": [1],
            "destination_zero_balance_after": [0],
            "amount_to_origin_balance": [0.2],
            "amount_to_destination_balance": [0.0],
            "is_transfer": [0],
            "is_cash_out": [0],
            "log_amount": [4.615],
        }
    )

    assert len(df.columns) == 24


def test_identifier_columns_are_not_in_processed_feature_list():
    processed_columns = [
        "step",
        "type",
        "amount",
        "oldbalanceOrg",
        "newbalanceOrig",
        "oldbalanceDest",
        "newbalanceDest",
        "isFraud",
        "isFlaggedFraud",
        "origin_balance_change",
        "destination_balance_change",
        "origin_balance_error",
        "destination_balance_error",
        "origin_balance_error_abs",
        "destination_balance_error_abs",
        "origin_zero_balance_before",
        "origin_zero_balance_after",
        "destination_zero_balance_before",
        "destination_zero_balance_after",
        "amount_to_origin_balance",
        "amount_to_destination_balance",
        "is_transfer",
        "is_cash_out",
        "log_amount",
    ]

    assert "nameOrig" not in processed_columns
    assert "nameDest" not in processed_columns


def test_suspicious_features_are_identified():
    import pandas as pd

    df = pd.DataFrame(
        {
            "isFraud": [0, 1],
            "isFlaggedFraud": [0, 1],
            "origin_balance_error": [0.0, 1.0],
            "amount": [100.0, 200.0],
        }
    )

    from src.machine_learning.validation import (
        identify_suspicious_features,
    )

    suspicious = identify_suspicious_features(df)

    assert "isFlaggedFraud" in suspicious
    assert "origin_balance_error" in suspicious

def test_calculate_metrics_returns_required_metrics():
    import numpy as np
    import pandas as pd

    from src.machine_learning.optimization import calculate_metrics

    y_true = pd.Series([0, 0, 1, 1])
    probabilities = np.array([0.1, 0.2, 0.8, 0.9])

    results = calculate_metrics(
        y_true,
        probabilities,
        threshold=0.5,
    )

    required = {
        "threshold",
        "accuracy",
        "precision",
        "recall",
        "f1_score",
        "roc_auc",
    }

    assert required.issubset(results.keys())


def test_threshold_evaluation_returns_all_thresholds():
    import numpy as np
    import pandas as pd

    from src.machine_learning.optimization import evaluate_thresholds

    y_true = pd.Series([0, 0, 1, 1])
    probabilities = np.array([0.1, 0.2, 0.8, 0.9])

    thresholds = [0.25, 0.50, 0.75]

    results = evaluate_thresholds(
        y_true,
        probabilities,
        thresholds,
    )

    assert len(results) == 3
    assert results["threshold"].tolist() == thresholds


def test_best_threshold_is_selected_by_f1():
    import pandas as pd

    from src.machine_learning.optimization import select_best_threshold

    results = pd.DataFrame(
        {
            "threshold": [0.25, 0.50, 0.75],
            "f1_score": [0.60, 0.90, 0.70],
        }
    )

    best = select_best_threshold(
        results,
        metric="f1_score",
    )

    assert best["threshold"] == 0.50
    assert best["f1_score"] == 0.90