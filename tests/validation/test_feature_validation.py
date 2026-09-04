"""
Phase 12 - Feature engineering validation tests.
"""

import numpy as np
import pandas as pd

from src.feature_engineering.features import (
    engineer_features,
    get_model_features,
)


def create_sample_dataset():
    df = pd.DataFrame(
        {
            "step": [1, 2, 3, 4, 5],
            "type": [
                "PAYMENT",
                "TRANSFER",
                "CASH_OUT",
                "DEBIT",
                "CASH_IN",
            ],
            "amount": [
                100.0,
                5000.0,
                2500.0,
                500.0,
                750.0,
            ],
            "oldbalanceOrg": [
                1000.0,
                10000.0,
                5000.0,
                2000.0,
                1000.0,
            ],
            "newbalanceOrig": [
                900.0,
                5000.0,
                2500.0,
                1500.0,
                1750.0,
            ],
            "oldbalanceDest": [
                500.0,
                1000.0,
                0.0,
                500.0,
                0.0,
            ],
            "newbalanceDest": [
                600.0,
                6000.0,
                0.0,
                500.0,
                0.0,
            ],
            "isFraud": [0, 0, 1, 0, 0],
            "isFlaggedFraud": [0, 0, 0, 0, 0],
        }
    )

    df["origin_balance_change"] = (
        df["oldbalanceOrg"] - df["newbalanceOrig"]
    )

    df["destination_balance_change"] = (
        df["newbalanceDest"] - df["oldbalanceDest"]
    )

    df["origin_balance_error"] = (
        df["oldbalanceOrg"]
        - df["amount"]
        - df["newbalanceOrig"]
    )

    df["destination_balance_error"] = (
        df["oldbalanceDest"]
        + df["amount"]
        - df["newbalanceDest"]
    )

    df["origin_balance_error_abs"] = (
        df["origin_balance_error"].abs()
    )

    df["destination_balance_error_abs"] = (
        df["destination_balance_error"].abs()
    )

    df["origin_zero_balance_before"] = (
        df["oldbalanceOrg"] == 0
    ).astype(int)

    df["is_transfer"] = (
        df["type"] == "TRANSFER"
    ).astype(int)

    df["is_cash_out"] = (
        df["type"] == "CASH_OUT"
    ).astype(int)

    df["log_amount"] = np.log1p(df["amount"])

    return df


def test_feature_engineering_preserves_row_count():
    df = create_sample_dataset()

    engineered = engineer_features(df)

    assert len(engineered) == len(df)


def test_feature_engineering_adds_features():
    df = create_sample_dataset()

    engineered = engineer_features(df)

    expected_features = {
        "origin_balance_change",
        "destination_balance_change",
        "origin_balance_error",
        "destination_balance_error",
        "origin_balance_error_abs",
        "destination_balance_error_abs",
        "origin_zero_balance_before",
        "is_transfer",
        "is_cash_out",
        "log_amount",
        "amount_to_origin_balance",
        "amount_to_destination_balance",
        "amount_log_ratio",
        "origin_balance_change_ratio",
        "origin_balance_utilization",
        "destination_balance_change_ratio",
        "high_origin_balance_error",
        "high_destination_balance_error",
        "is_large_transaction",
        "is_zero_origin_before_withdrawal",
        "step_mod_24",
        "is_late_step",
        "transfer_or_cashout",
        "large_transfer_or_cashout",
    }

    assert expected_features.issubset(set(engineered.columns))


def test_model_features_have_expected_count():
    df = create_sample_dataset()

    engineered = engineer_features(df)

    features = get_model_features(
        engineered,
        include_flagged_fraud=False,
    )

    assert isinstance(features, list)
    assert len(features) == 30


def test_target_is_not_a_model_feature():
    df = create_sample_dataset()

    engineered = engineer_features(df)

    features = get_model_features(
        engineered,
        include_flagged_fraud=False,
    )

    assert "isFraud" not in features


def test_transaction_type_is_not_a_model_feature():
    df = create_sample_dataset()

    engineered = engineer_features(df)

    features = get_model_features(
        engineered,
        include_flagged_fraud=False,
    )

    assert "type" not in features


def test_flagged_fraud_is_not_a_model_feature_by_default():
    df = create_sample_dataset()

    engineered = engineer_features(df)

    features = get_model_features(
        engineered,
        include_flagged_fraud=False,
    )

    assert "isFlaggedFraud" not in features
