"""
Tests for fraud investigation utilities.
"""

import pytest

from app.utils import (
    get_investigation_priority,
    get_priority_description,
)


@pytest.mark.parametrize(
    "probability,expected",
    [
        (0.00, "Low"),
        (0.10, "Low"),
        (0.2499, "Low"),
        (0.25, "Moderate"),
        (0.40, "Moderate"),
        (0.4999, "Moderate"),
        (0.50, "High"),
        (0.65, "High"),
        (0.7499, "High"),
        (0.75, "Critical"),
        (0.90, "Critical"),
        (1.00, "Critical"),
    ],
)
def test_investigation_priority(
    probability,
    expected,
):
    assert (
        get_investigation_priority(probability)
        == expected
    )


@pytest.mark.parametrize(
    "probability",
    [
        -0.01,
        1.01,
        2.0,
    ],
)
def test_invalid_probability(
    probability,
):
    with pytest.raises(ValueError):
        get_investigation_priority(
            probability
        )


def test_priority_description():
    description = get_priority_description(
        "Critical"
    )

    assert isinstance(description, str)
    assert len(description) > 0


def test_invalid_priority_description():
    with pytest.raises(ValueError):
        get_priority_description(
            "Unknown"
        )
