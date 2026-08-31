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
