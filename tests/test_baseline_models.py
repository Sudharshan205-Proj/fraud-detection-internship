import pandas as pd
import pytest  # noqa: F401

from src.machine_learning.evaluation import evaluate_model
from src.machine_learning.models import (
    create_logistic_regression,
    create_random_forest,
    train_model,
)


def test_logistic_regression_creation():
    model = create_logistic_regression()

    assert model is not None
    assert model.__class__.__name__ == "LogisticRegression"


def test_random_forest_creation():
    model = create_random_forest()

    assert model is not None
    assert model.__class__.__name__ == "RandomForestClassifier"


def test_logistic_regression_has_balanced_class_weight():
    model = create_logistic_regression()

    assert model.class_weight == "balanced"


def test_random_forest_has_balanced_class_weight():
    model = create_random_forest()

    assert model.class_weight == "balanced"


def test_train_model():
    X_train = pd.DataFrame(
        {
            "feature_1": [1, 2, 3, 4],
            "feature_2": [4, 3, 2, 1],
        }
    )

    y_train = pd.Series([0, 0, 1, 1])

    model = create_logistic_regression()

    trained_model = train_model(
        model,
        X_train,
        y_train,
    )

    assert hasattr(trained_model, "predict")


def test_evaluate_model():
    X_train = pd.DataFrame(
        {
            "feature_1": [1, 2, 3, 4, 5, 6],
            "feature_2": [6, 5, 4, 3, 2, 1],
        }
    )

    y_train = pd.Series([0, 0, 0, 1, 1, 1])

    X_test = pd.DataFrame(
        {
            "feature_1": [1.5, 5.5],
            "feature_2": [5.5, 1.5],
        }
    )

    y_test = pd.Series([0, 1])

    model = create_logistic_regression()

    model = train_model(
        model,
        X_train,
        y_train,
    )

    metrics = evaluate_model(
        model,
        X_test,
        y_test,
    )

    assert "accuracy" in metrics
    assert "precision" in metrics
    assert "recall" in metrics
    assert "f1_score" in metrics
    assert "roc_auc" in metrics

    for value in metrics.values():
        assert 0 <= value <= 1
