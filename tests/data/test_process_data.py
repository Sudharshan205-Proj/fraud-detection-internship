import pandas as pd
import pytest

from src.data_processing.process_data import (
    ENGINEERED_COLUMNS,
    EXPECTED_COLUMNS,
    EXPECTED_TRANSACTION_TYPES,
    PROCESSED_COLUMNS,
    engineer_features,
    load_data,
    load_processed_dataset,
    process_dataset,
    validate_raw_data,
    validate_schema,
    validate_values,
)


@pytest.fixture
def sample_raw_data():
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


def test_raw_schema_matches_paysim(sample_raw_data):
    assert list(sample_raw_data.columns) == EXPECTED_COLUMNS


def test_schema_validation_passes(sample_raw_data):
    validate_schema(sample_raw_data)


def test_schema_validation_rejects_missing_column(sample_raw_data):
    incomplete = sample_raw_data.drop(columns=["type"])

    with pytest.raises(ValueError):
        validate_schema(incomplete)


def test_schema_validation_rejects_wrong_order(sample_raw_data):
    reordered = sample_raw_data[list(reversed(EXPECTED_COLUMNS))]

    with pytest.raises(ValueError):
        validate_schema(reordered)


def test_expected_transaction_types():
    assert EXPECTED_TRANSACTION_TYPES == {
        "PAYMENT",
        "TRANSFER",
        "CASH_OUT",
        "CASH_IN",
        "DEBIT",
    }


def test_validation_passes_on_clean_data(sample_raw_data):
    results = validate_values(sample_raw_data)

    assert results == {
        "missing_values": 0,
        "duplicate_rows": 0,
        "invalid_transaction_types": 0,
        "invalid_isFraud_values": 0,
        "invalid_isFlaggedFraud_values": 0,
        "negative_financial_values": 0,
        "empty_origin_ids": 0,
        "empty_destination_ids": 0,
    }


def test_validation_rejects_negative_amounts(sample_raw_data):
    bad = sample_raw_data.copy()
    bad.loc[0, "amount"] = -50.0

    with pytest.raises(ValueError):
        validate_values(bad)


def test_validation_rejects_unknown_transaction_types(sample_raw_data):
    bad = sample_raw_data.copy()
    bad.loc[0, "type"] = "UNKNOWN"

    with pytest.raises(ValueError):
        validate_values(bad)


def test_validation_rejects_empty_identifiers(sample_raw_data):
    bad = sample_raw_data.copy()
    bad.loc[0, "nameOrig"] = "   "

    with pytest.raises(ValueError):
        validate_values(bad)


def test_validate_raw_data_wrapper(sample_raw_data):
    validate_raw_data(sample_raw_data)


def test_engineer_features_creates_all_15_features(sample_raw_data):
    processed = engineer_features(sample_raw_data)

    assert len(ENGINEERED_COLUMNS) == 15

    for column in ENGINEERED_COLUMNS:
        assert column in processed.columns


def test_engineer_features_preserves_row_count(sample_raw_data):
    processed = engineer_features(sample_raw_data)

    assert len(processed) == len(sample_raw_data)


def test_processed_dataset_has_24_columns(sample_raw_data):
    processed = process_dataset(sample_raw_data)

    assert len(processed.columns) == 24
    assert list(processed.columns) == PROCESSED_COLUMNS


def test_identifier_columns_are_removed_by_default(sample_raw_data):
    processed = process_dataset(sample_raw_data)

    assert "nameOrig" not in processed.columns
    assert "nameDest" not in processed.columns


def test_identifier_columns_can_be_kept(sample_raw_data):
    processed = process_dataset(
        sample_raw_data,
        drop_identifiers=False,
    )

    assert "nameOrig" in processed.columns
    assert "nameDest" in processed.columns


def test_target_is_preserved(sample_raw_data):
    processed = process_dataset(sample_raw_data)

    assert "isFraud" in processed.columns


def test_balance_features(sample_raw_data):
    processed = engineer_features(sample_raw_data)

    # Row 0: 1000 -> 900 with amount 100.
    assert processed.loc[0, "origin_balance_change"] == 100.0
    assert processed.loc[0, "origin_balance_error"] == 0.0

    # Row 1: destination balance 1000 -> 1500 with amount 500.
    assert processed.loc[1, "destination_balance_change"] == 500.0
    assert processed.loc[1, "destination_balance_error"] == 0.0

    # Row 0: no destination movement at all.
    assert processed.loc[0, "destination_balance_change"] == 0.0
    assert processed.loc[0, "destination_balance_error"] == -100.0


def test_indicator_features(sample_raw_data):
    processed = engineer_features(sample_raw_data)

    assert processed.loc[1, "is_transfer"] == 1
    assert processed.loc[2, "is_cash_out"] == 1
    assert processed.loc[0, "is_transfer"] == 0

    # Rows 1-2 end with a zero origin balance.
    assert processed.loc[1, "origin_zero_balance_before"] == 0
    assert processed.loc[1, "origin_zero_balance_after"] == 1
    assert processed.loc[2, "origin_zero_balance_after"] == 1


def test_log_amount_is_non_negative(sample_raw_data):
    processed = engineer_features(sample_raw_data)

    assert (processed["log_amount"] >= 0).all()


def test_indicator_flags_are_downcast(sample_raw_data):
    processed = process_dataset(sample_raw_data)

    assert processed["isFraud"].dtype.name == "int8"
    assert processed["isFlaggedFraud"].dtype.name == "int8"
    assert processed["is_transfer"].dtype.name == "int8"


def test_load_data_from_csv(tmp_path, sample_raw_data):
    path = tmp_path / "raw.csv"
    sample_raw_data.to_csv(path, index=False)

    loaded = load_data(path)

    assert list(loaded.columns) == EXPECTED_COLUMNS
    assert len(loaded) == 3


def test_load_data_respects_max_rows(tmp_path, sample_raw_data):
    path = tmp_path / "raw.csv"
    sample_raw_data.to_csv(path, index=False)

    loaded = load_data(path, max_rows=2)

    assert len(loaded) == 2


def test_load_data_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_data(tmp_path / "does-not-exist.csv")


def test_load_processed_dataset_round_trip(tmp_path, sample_raw_data):
    path = tmp_path / "processed.csv"
    processed = process_dataset(sample_raw_data)
    processed.to_csv(path, index=False)

    loaded = load_processed_dataset(path, max_rows=2)

    assert list(loaded.columns) == PROCESSED_COLUMNS
    assert len(loaded) == 2


def test_load_processed_dataset_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_processed_dataset(tmp_path / "does-not-exist.csv")
