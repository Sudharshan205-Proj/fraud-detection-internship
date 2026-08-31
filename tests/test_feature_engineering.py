import pandas as pd
import pytest

from src.feature_engineering.features import (
    engineer_features,
    get_model_features,
)


@pytest.fixture
def sample_data():
    return pd.DataFrame(
        {
            "step": [1, 10, 500, 700],
            "type": ["PAYMENT", "TRANSFER", "CASH_OUT", "TRANSFER"],
            "amount": [100.0, 5000.0, 100000.0, 200000.0],
            "oldbalanceOrg": [1000.0, 5000.0, 100000.0, 200000.0],
            "newbalanceOrig": [900.0, 0.0, 0.0, 0.0],
            "oldbalanceDest": [0.0, 1000.0, 50000.0, 100000.0],
            "newbalanceDest": [0.0, 6000.0, 150000.0, 300000.0],
            "isFraud": [0, 1, 1, 0],
            "isFlaggedFraud": [0, 0, 1, 0],
            "origin_balance_change": [-100.0, -5000.0, -100000.0, -200000.0],
            "destination_balance_change": [0.0, 5000.0, 100000.0, 200000.0],
            "origin_balance_error": [0.0, 0.0, 0.0, 0.0],
            "destination_balance_error": [0.0, 0.0, 0.0, 0.0],
            "origin_balance_error_abs": [0.0, 0.0, 0.0, 0.0],
            "destination_balance_error_abs": [0.0, 0.0, 0.0, 0.0],
            "origin_zero_balance_before": [0, 0, 0, 0],
            "origin_zero_balance_after": [0, 1, 1, 1],
            "destination_zero_balance_before": [1, 0, 0, 0],
            "destination_zero_balance_after": [1, 0, 0, 0],
            "amount_to_origin_balance": [0.1, 0.8333, 0.99, 0.995],
            "amount_to_destination_balance": [100.0, 4.995, 1.96, 1.98],
            "is_transfer": [0, 1, 0, 1],
            "is_cash_out": [0, 0, 1, 0],
            "log_amount": [4.615, 8.517, 11.513, 12.206],
        }
    )


def test_feature_engineering_preserves_rows(sample_data):
    result = engineer_features(sample_data)

    assert len(result) == len(sample_data)


def test_feature_engineering_preserves_original_columns(sample_data):
    result = engineer_features(sample_data)

    for column in sample_data.columns:
        assert column in result.columns


def test_new_features_are_created(sample_data):
    result = engineer_features(sample_data)

    expected_features = [
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
    ]

    for feature in expected_features:
        assert feature in result.columns


def test_engineered_features_are_numeric(sample_data):
    result = engineer_features(sample_data)

    numeric_features = [
        "amount_log_ratio",
        "origin_balance_change_ratio",
        "origin_balance_utilization",
        "destination_balance_change_ratio",
        "high_origin_balance_error",
        "high_destination_balance_error",
        "is_large_transaction",
        "step_mod_24",
        "is_late_step",
        "transfer_or_cashout",
        "large_transfer_or_cashout",
    ]

    for feature in numeric_features:
        assert pd.api.types.is_numeric_dtype(result[feature])


def test_no_missing_values_created(sample_data):
    result = engineer_features(sample_data)

    assert result.isnull().sum().sum() == 0


def test_target_is_excluded_from_model_features(sample_data):
    result = engineer_features(sample_data)

    features = get_model_features(result)

    assert "isFraud" not in features


def test_account_identifiers_are_excluded(sample_data):
    result = engineer_features(sample_data)

    features = get_model_features(result)

    assert "nameOrig" not in features
    assert "nameDest" not in features


def test_flagged_fraud_excluded_by_default(sample_data):
    result = engineer_features(sample_data)

    features = get_model_features(result)

    assert "isFlaggedFraud" not in features


def test_flagged_fraud_can_be_explicitly_included(sample_data):
    result = engineer_features(sample_data)

    features = get_model_features(
        result,
        include_flagged_fraud=True,
    )

    assert "isFlaggedFraud" in features


def test_transfer_or_cashout_feature(sample_data):
    result = engineer_features(sample_data)

    assert result.loc[1, "transfer_or_cashout"] == 1
    assert result.loc[2, "transfer_or_cashout"] == 1
    assert result.loc[0, "transfer_or_cashout"] == 0


def test_missing_required_columns_raise_error():
    incomplete = pd.DataFrame(
        {
            "step": [1],
            "amount": [100.0],
        }
    )

    with pytest.raises(ValueError):
        engineer_features(incomplete)
