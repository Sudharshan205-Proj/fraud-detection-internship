"""
Phase 12 - Final model validation tests.
"""

import json

from app.model_services import FraudModelService

EXPECTED_FEATURE_COUNT = 33


def test_final_model_loads():
    service = FraudModelService()

    assert service.model is not None


def test_final_model_is_random_forest():
    service = FraudModelService()

    assert (
        type(service.model).__name__
        == "RandomForestClassifier"
    )


def test_final_model_has_expected_feature_count():
    service = FraudModelService()

    assert len(service.feature_columns) == (
        EXPECTED_FEATURE_COUNT
    )

    assert service.model.n_features_in_ == (
        EXPECTED_FEATURE_COUNT
    )


def test_feature_schema_is_unique():
    service = FraudModelService()

    assert len(service.feature_columns) == len(
        set(service.feature_columns)
    )


def test_feature_schema_contains_no_target():
    service = FraudModelService()

    assert "isFraud" not in service.feature_columns


def test_feature_schema_contains_no_transaction_type():
    service = FraudModelService()

    assert "type" not in service.feature_columns


def test_inference_thresholds_exist():
    service = FraudModelService()

    assert (
        "large_transaction_amount"
        in service.inference_thresholds
    )

    assert (
        "late_step"
        in service.inference_thresholds
    )


def test_inference_thresholds_are_numeric():
    service = FraudModelService()

    assert isinstance(
        service.inference_thresholds[
            "large_transaction_amount"
        ],
        (int, float),
    )

    assert isinstance(
        service.inference_thresholds["late_step"],
        (int, float),
    )


def test_feature_schema_matches_saved_json():
    service = FraudModelService()

    with open(
        "models/model_features.json",
        "r",
        encoding="utf-8",
    ) as file:
        schema = json.load(file)

    assert schema["features"] == (
        service.feature_columns
    )