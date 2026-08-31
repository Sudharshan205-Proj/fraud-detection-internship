import pandas as pd
import pytest

from src.data.process_data import (
    engineer_features,
    remove_identifier_columns,
    validate_raw_data,
)


@pytest.fixture
def sample_data():
    return pd.DataFrame(
        {
            "step": [1, 2, 3],
            "type": ["PAYMENT", "TRANSFER", "CASH_OUT"],
            "amount": [100.0, 500.0, 200.0],
            "nameOrig": ["C1", "C2", "C3"],
            "oldbalanceOrg": [1000.0, 500.0, 200.0],
            "newbalanceOrig": [900.0, 0.0, 0.0],
            "nameDest": ["M1", "C4", "C5"],
            "oldbalanceDest": [0.0, 1000.0, 500.0],
            "newbalanceDest": [0.0, 1500.0, 700.0],
            "isFraud": [0, 1, 1],
            "isFlaggedFraud": [0, 0, 0],
        }
    )


def test_validation_passes(sample_data):
    validate_raw_data(sample_data)


def test_feature_engineering_creates_expected_columns(sample_data):
    processed = engineer_features(sample_data)

    expected_columns = [
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

    for column in expected_columns:
        assert column in processed.columns


def test_feature_engineering_preserves_row_count(sample_data):
    processed = engineer_features(sample_data)

    assert len(processed) == len(sample_data)


def test_identifier_columns_are_removed(sample_data):
    processed = engineer_features(sample_data)
    processed = remove_identifier_columns(processed)

    assert "nameOrig" not in processed.columns
    assert "nameDest" not in processed.columns


def test_target_is_preserved(sample_data):
    processed = engineer_features(sample_data)
    processed = remove_identifier_columns(processed)

    assert "isFraud" in processed.columns


def test_transaction_flags(sample_data):
    processed = engineer_features(sample_data)

    assert processed.loc[1, "is_transfer"] == 1
    assert processed.loc[2, "is_cash_out"] == 1
    assert processed.loc[0, "is_transfer"] == 0


def test_log_amount_is_non_negative(sample_data):
    processed = engineer_features(sample_data)

    assert (processed["log_amount"] >= 0).all()
