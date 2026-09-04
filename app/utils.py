"""
Application utilities for fraud investigation.

Provides human-readable investigation priority levels based
on model-estimated fraud probability.
"""

from __future__ import annotations


def get_investigation_priority(
    fraud_probability: float,
) -> str:
    """
    Convert fraud probability into an investigation priority.

    Priority thresholds are intended for analyst triage and
    are not equivalent to proof of fraud.
    """

    if not 0.0 <= fraud_probability <= 1.0:
        raise ValueError(
            "Fraud probability must be between 0 and 1."
        )

    if fraud_probability >= 0.75:
        return "Critical"

    if fraud_probability >= 0.50:
        return "High"

    if fraud_probability >= 0.25:
        return "Moderate"

    return "Low"


def get_priority_description(
    priority: str,
) -> str:
    """
    Return an analyst-friendly explanation of a priority level.
    """

    descriptions = {
        "Critical": (
            "Very high model-estimated fraud probability. "
            "Prioritize this transaction for immediate review."
        ),
        "High": (
            "High model-estimated fraud probability. "
            "Review this transaction promptly."
        ),
        "Moderate": (
            "Moderate model-estimated fraud probability. "
            "Consider additional review alongside other signals."
        ),
        "Low": (
            "Low model-estimated fraud probability. "
            "No immediate priority is indicated by this model."
        ),
    }

    if priority not in descriptions:
        raise ValueError(
            f"Unknown investigation priority: {priority}"
        )

    return descriptions[priority]
