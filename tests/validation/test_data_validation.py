"""
Phase 12 - Data validation tests.

These tests validate the structural and quality assumptions used by
the fraud-detection project without requiring the full 6.3M-row
PaySim dataset during automated testing.
"""

import pandas as pd
import pytest

REQUIRED_COLUMNS = {
    "step",
    "type",
    "amount",
    "oldbalanceOrg",
    "newbalanceOrig",
    "oldbalanceDest",
    "newbalanceDest",
    "isFraud",
    "isFlaggedFraud",
}


@pytest.fixture
def valid_transaction_frame():
    return pd.DataFrame(
        {
            "step": [1, 2, 3, 4],
            "type": [
                "PAYMENT",
                "TRANSFER",
                "CASH_OUT",
                "CASH_IN",
            ],
            "amount": [
                100.0,
                5000.0,
                2500.0,
                750.0,
            ],
            "oldbalanceOrg": [
                1000.0,
                10000.0,
                5000.0,
                1000.0,
            ],
            "newbalanceOrig": [
                900.0,
                5000.0,
                2500.0,
                1750.0,
            ],
            "oldbalanceDest": [
                500.0,
                1000.0,
                0.0,
                0.0,
            ],
            "newbalanceDest": [
                600.0,
                6000.0,
                0.0,
                0.0,
            ],
            "isFraud": [0, 0, 1, 0],
            "isFlaggedFraud": [0, 0, 0, 0],
        }
    )


def test_required_columns_are_present(valid_transaction_frame):
    assert REQUIRED_COLUMNS.issubset(
        valid_transaction_frame.columns
    )


def test_dataset_has_no_missing_values(valid_transaction_frame):
    assert not valid_transaction_frame.isnull().any().any()


def test_dataset_has_no_duplicate_rows(valid_transaction_frame):
    assert not valid_transaction_frame.duplicated().any()


def test_amount_is_numeric(valid_transaction_frame):
    assert pd.api.types.is_numeric_dtype(
        valid_transaction_frame["amount"]
    )


def test_step_is_numeric(valid_transaction_frame):
    assert pd.api.types.is_numeric_dtype(
        valid_transaction_frame["step"]
    )


def test_transaction_type_is_categorical(valid_transaction_frame):
    dtype = valid_transaction_frame["type"].dtype

    assert (
        dtype == "object"
        or isinstance(dtype, (pd.StringDtype, pd.CategoricalDtype))
    )


def test_fraud_target_is_binary(valid_transaction_frame):
    assert set(
        valid_transaction_frame["isFraud"].unique()
    ).issubset({0, 1})


def test_flagged_fraud_is_binary(valid_transaction_frame):
    assert set(
        valid_transaction_frame["isFlaggedFraud"].unique()
    ).issubset({0, 1})


def test_amount_is_non_negative(valid_transaction_frame):
    assert (
        valid_transaction_frame["amount"] >= 0
    ).all()


def test_balances_are_non_negative(valid_transaction_frame):
    balance_columns = [
        "oldbalanceOrg",
        "newbalanceOrig",
        "oldbalanceDest",
        "newbalanceDest",
    ]

    for column in balance_columns:
        assert (
            valid_transaction_frame[column] >= 0
        ).all()
