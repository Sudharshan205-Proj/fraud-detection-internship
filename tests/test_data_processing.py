import pandas as pd

from src.data_processing.process_data import (
    EXPECTED_COLUMNS,
    EXPECTED_TRANSACTION_TYPES,
    process_dataset,
    validate_schema,
    validate_values,
)


def test_expected_columns():
    df = pd.DataFrame(
        {
            "step": [1],
            "type": ["PAYMENT"],
            "amount": [100.0],
            "nameOrig": ["C1"],
            "oldbalanceOrg": [200.0],
            "newbalanceOrig": [100.0],
            "nameDest": ["M1"],
            "oldbalanceDest": [0.0],
            "newbalanceDest": [100.0],
            "isFraud": [0],
            "isFlaggedFraud": [0],
        }
    )

    assert list(df.columns) == EXPECTED_COLUMNS


def test_schema_validation():
    df = pd.DataFrame(
        {
            "step": [1],
            "type": ["PAYMENT"],
            "amount": [100.0],
            "nameOrig": ["C1"],
            "oldbalanceOrg": [200.0],
            "newbalanceOrig": [100.0],
            "nameDest": ["M1"],
            "oldbalanceDest": [0.0],
            "newbalanceDest": [100.0],
            "isFraud": [0],
            "isFlaggedFraud": [0],
        }
    )

    validate_schema(df)


def test_valid_transaction_types():
    assert EXPECTED_TRANSACTION_TYPES == {
        "PAYMENT",
        "TRANSFER",
        "CASH_OUT",
        "CASH_IN",
        "DEBIT",
    }


def test_no_missing_values():
    df = pd.DataFrame(
        {
            "step": [1],
            "type": ["PAYMENT"],
            "amount": [100.0],
            "nameOrig": ["C1"],
            "oldbalanceOrg": [200.0],
            "newbalanceOrig": [100.0],
            "nameDest": ["M1"],
            "oldbalanceDest": [0.0],
            "newbalanceDest": [100.0],
            "isFraud": [0],
            "isFlaggedFraud": [0],
        }
    )

    results = validate_values(df)

    assert results["missing_values"] == 0


def test_process_creates_balance_features():
    df = pd.DataFrame(
        {
            "step": [1],
            "type": ["PAYMENT"],
            "amount": [100.0],
            "nameOrig": ["C1"],
            "oldbalanceOrg": [200.0],
            "newbalanceOrig": [100.0],
            "nameDest": ["M1"],
            "oldbalanceDest": [0.0],
            "newbalanceDest": [100.0],
            "isFraud": [0],
            "isFlaggedFraud": [0],
        }
    )

    processed = process_dataset(df)

    assert "origin_balance_change" in processed.columns
    assert "destination_balance_change" in processed.columns
    assert "origin_balance_error" in processed.columns
    assert "destination_balance_error" in processed.columns

    assert processed.loc[0, "origin_balance_change"] == 100.0
    assert processed.loc[0, "destination_balance_change"] == 100.0
    assert processed.loc[0, "origin_balance_error"] == 0.0
    assert processed.loc[0, "destination_balance_error"] == 0.0
