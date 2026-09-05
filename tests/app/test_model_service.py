"""
Tests for the Phase 10 fraud-model inference service.
"""

import pytest

from app.model_services import FraudModelService


@pytest.fixture
def model_service():
    return FraudModelService()


@pytest.fixture
def sample_transaction():
    return {
        "step": 1,
        "type": "PAYMENT",
        "amount": 1000.0,
        "oldbalanceOrg": 5000.0,
        "newbalanceOrig": 4000.0,
        "oldbalanceDest": 1000.0,
        "newbalanceDest": 2000.0,
    }


def test_model_service_loads(model_service):
    assert model_service.model is not None


def test_model_has_expected_feature_count(model_service):
    assert len(model_service.feature_columns) == 33
    assert model_service.model.n_features_in_ == 33


def test_prepare_transaction_shape(
    model_service,
    sample_transaction,
):
    X = model_service.prepare_transaction(
        sample_transaction
    )

    assert X.shape == (1, 33)


def test_prepare_transaction_columns(
    model_service,
    sample_transaction,
):
    X = model_service.prepare_transaction(
        sample_transaction
    )

    assert list(X.columns) == (
        model_service.feature_columns
    )


def test_prediction(
    model_service,
    sample_transaction,
):
    result = model_service.predict(
        sample_transaction
    )

    assert "prediction" in result
    assert "fraud_probability" in result

    assert result["prediction"] in (0, 1)

    assert (
        0.0
        <= result["fraud_probability"]
        <= 1.0
    )


def test_missing_transaction_field(
    model_service,
):
    transaction = {
        "step": 1,
        "type": "PAYMENT",
        "amount": 1000.0,
    }

    with pytest.raises(ValueError):
        model_service.prepare_transaction(
            transaction
        )
