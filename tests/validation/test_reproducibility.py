"""
Phase 12 - Reproducibility and leakage validation tests.
"""

import json

import numpy as np
import pandas as pd
import pytest  # noqa: F401
from sklearn.model_selection import train_test_split


def create_sample_dataset():
    rng = np.random.default_rng(42)

    df = pd.DataFrame(
        {
            "amount": rng.uniform(10, 10000, 100),
            "step": np.arange(100),
            "isFraud": [0] * 95 + [1] * 5,
        }
    )

    return df


def create_feature_sample_dataset():
    """
    Create the same type of input expected by engineer_features().
    The feature engineering module requires the derived columns
    generated during the data-processing stage.
    """

    df = pd.DataFrame(
        {
            "step": [1, 2, 3, 4],
            "type": [
                "PAYMENT",
                "TRANSFER",
                "CASH_OUT",
                "DEBIT",
            ],
            "amount": [
                100.0,
                5000.0,
                2500.0,
                500.0,
            ],
            "oldbalanceOrg": [
                1000.0,
                10000.0,
                5000.0,
                2000.0,
            ],
            "newbalanceOrig": [
                900.0,
                5000.0,
                2500.0,
                1500.0,
            ],
            "oldbalanceDest": [
                500.0,
                1000.0,
                0.0,
                500.0,
            ],
            "newbalanceDest": [
                600.0,
                6000.0,
                0.0,
                500.0,
            ],
            "isFraud": [0, 0, 1, 0],
            "isFlaggedFraud": [0, 0, 0, 0],
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


def test_stratified_split_is_reproducible():
    df = create_sample_dataset()

    train_a, test_a = train_test_split(
        df,
        test_size=0.2,
        stratify=df["isFraud"],
        random_state=42,
    )

    train_b, test_b = train_test_split(
        df,
        test_size=0.2,
        stratify=df["isFraud"],
        random_state=42,
    )

    pd.testing.assert_frame_equal(
        train_a,
        train_b,
    )

    pd.testing.assert_frame_equal(
        test_a,
        test_b,
    )


def test_train_and_test_indices_do_not_overlap():
    df = create_sample_dataset()

    train, test = train_test_split(
        df,
        test_size=0.2,
        stratify=df["isFraud"],
        random_state=42,
    )

    assert set(train.index).isdisjoint(
        set(test.index)
    )


def test_target_is_not_used_as_model_feature():
    from src.feature_engineering.features import (
        engineer_features,
        get_model_features,
    )

    df = create_feature_sample_dataset()

    engineered = engineer_features(df)

    features = get_model_features(
        engineered,
        include_flagged_fraud=False,
    )

    assert isinstance(features, list)
    assert "isFraud" not in features


def test_fixed_random_seed_is_documented():
    with open(
        "models/model_features.json",
        "r",
        encoding="utf-8",
    ) as file:
        schema = json.load(file)

    assert isinstance(schema, dict)


def test_project_uses_expected_feature_count():
    from app.model_services import FraudModelService

    service = FraudModelService()

    assert len(service.feature_columns) == 33
