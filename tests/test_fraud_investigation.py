import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from src.analysis.fraud_investigation import (
    create_investigation_report,
    prepare_features,
    save_investigation_report,
    train_investigation_model,
)
from src.machine_learning.explainability import get_feature_importance


def create_sample_data():
    return pd.DataFrame(
        {
            "step": [1, 2, 3, 4, 5, 6],
            "type": [
                "PAYMENT",
                "PAYMENT",
                "TRANSFER",
                "TRANSFER",
                "CASH_OUT",
                "CASH_OUT",
            ],
            "amount": [
                10,
                20,
                100,
                200,
                500,
                1000,
            ],
            "balance": [
                100,
                90,
                200,
                100,
                500,
                0,
            ],
            "isFraud": [
                0,
                0,
                0,
                1,
                1,
                1,
            ],
        }
    )


def test_prepare_features():
    df = create_sample_data()

    X, y = prepare_features(df)

    assert isinstance(X, pd.DataFrame)
    assert isinstance(y, pd.Series)

    assert "isFraud" not in X.columns
    assert len(X) == len(y)


def test_train_investigation_model():
    df = create_sample_data()

    X, y = prepare_features(df)

    model = train_investigation_model(
        X,
        y,
    )

    assert isinstance(
        model,
        RandomForestClassifier,
    )


def test_create_investigation_report():
    df = create_sample_data()

    X, y = prepare_features(df)

    model = train_investigation_model(
        X,
        y,
    )

    importance = get_feature_importance(
        model,
        X.columns,
    )

    report = create_investigation_report(
        model,
        X,
        df,
        importance,
    )

    assert isinstance(
        report,
        pd.DataFrame,
    )

    assert "fraud_probability" in report.columns
    assert "predicted_fraud" in report.columns
    assert "investigation_priority" in report.columns


def test_investigation_report_sorted():
    df = create_sample_data()

    X, y = prepare_features(df)

    model = train_investigation_model(
        X,
        y,
    )

    importance = get_feature_importance(
        model,
        X.columns,
    )

    report = create_investigation_report(
        model,
        X,
        df,
        importance,
    )

    probabilities = report[
        "fraud_probability"
    ].tolist()

    assert probabilities == sorted(
        probabilities,
        reverse=True,
    )


def test_save_investigation_report(tmp_path):
    df = create_sample_data()

    X, y = prepare_features(df)

    model = train_investigation_model(
        X,
        y,
    )

    importance = get_feature_importance(
        model,
        X.columns,
    )

    report = create_investigation_report(
        model,
        X,
        df,
        importance,
    )

    output_file = (
        tmp_path
        / "investigation.csv"
    )

    save_investigation_report(
        report,
        output_file,
    )

    assert output_file.exists()
