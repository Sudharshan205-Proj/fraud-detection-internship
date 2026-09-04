"""
Phase 12 - Application and inference validation tests.
"""

import pytest

from app.model_service import FraudModelService
from app.utils import (
    get_investigation_priority,
    get_priority_description,
)


@pytest.fixture
def service():
    return FraudModelService()


@pytest.fixture
def valid_transaction():
    return {
        "step": 1,
        "type": "PAYMENT",
        "amount": 1000.0,
        "oldbalanceOrg": 5000.0,
        "newbalanceOrig": 4000.0,
        "oldbalanceDest": 1000.0,
        "newbalanceDest": 2000.0,
    }


@pytest.mark.parametrize(
    "transaction_type",
    [
        "PAYMENT",
        "TRANSFER",
        "CASH_OUT",
        "DEBIT",
        "CASH_IN",
    ],
)
def test_all_transaction_types_are_supported(
    service,
    valid_transaction,
    transaction_type,
):
    transaction = valid_transaction.copy()
    transaction["type"] = transaction_type

    result = service.predict(transaction)

    assert result["prediction"] in (0, 1)
    assert 0.0 <= result["fraud_probability"] <= 1.0


def test_prediction_result_contains_required_fields(
    service,
    valid_transaction,
):
    result = service.predict(valid_transaction)

    assert set(
        result.keys()
    ) >= {
        "prediction",
        "fraud_probability",
    }


def test_prediction_is_integer(
    service,
    valid_transaction,
):
    result = service.predict(valid_transaction)

    assert result["prediction"] in (0, 1)


def test_probability_is_float(
    service,
    valid_transaction,
):
    result = service.predict(valid_transaction)

    assert isinstance(
        result["fraud_probability"],
        float,
    )


def test_priority_mapping_is_valid():
    priorities = {
        get_investigation_priority(0.10),
        get_investigation_priority(0.30),
        get_investigation_priority(0.60),
        get_investigation_priority(0.80),
    }

    assert priorities == {
        "Low",
        "Moderate",
        "High",
        "Critical",
    }


def test_priority_description_exists():
    priority = get_investigation_priority(0.80)

    description = get_priority_description(
        priority
    )

    assert isinstance(description, str)
    assert len(description) > 0


def test_invalid_probability_is_rejected():
    with pytest.raises(ValueError):
        get_investigation_priority(-0.1)

    with pytest.raises(ValueError):
        get_investigation_priority(1.1)


def test_missing_field_is_rejected(service):
    transaction = {
        "step": 1,
        "type": "PAYMENT",
        "amount": 1000.0,
    }

    with pytest.raises(ValueError):
        service.predict(transaction)


def test_streamlit_module_imports():
    import app.streamlit_app

    assert app.streamlit_app.main is not None
