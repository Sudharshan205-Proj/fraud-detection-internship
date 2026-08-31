"""
Feature engineering utilities for the fraud detection project.

This module creates additional behavioural and transaction-level
features from the processed PaySim dataset.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

REQUIRED_COLUMNS = [
    "step",
    "type",
    "amount",
    "oldbalanceOrg",
    "newbalanceOrig",
    "oldbalanceDest",
    "newbalanceDest",
    "isFraud",
    "isFlaggedFraud",
]


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create additional fraud-detection features.

    Parameters
    ----------
    df:
        Processed PaySim DataFrame.

    Returns
    -------
    pd.DataFrame
        DataFrame containing the original columns plus engineered features.
    """

    missing_columns = [
        column for column in REQUIRED_COLUMNS if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    result = df.copy()

    # ------------------------------------------------------------
    # Transaction amount features
    # ------------------------------------------------------------

    result["amount_log_ratio"] = np.log1p(result["amount"])

    result["amount_to_origin_balance"] = (
        result["amount"]
        / (result["oldbalanceOrg"] + 1)
    )

    result["amount_to_destination_balance"] = (
        result["amount"]
        / (result["oldbalanceDest"] + 1)
    )

    # ------------------------------------------------------------
    # Origin account behaviour
    # ------------------------------------------------------------

    result["origin_balance_change_ratio"] = (
        result["origin_balance_change"].abs()
        / (result["oldbalanceOrg"] + 1)
    )

    result["origin_balance_utilization"] = (
        result["amount"]
        / (result["oldbalanceOrg"] + result["amount"] + 1)
    )

    # ------------------------------------------------------------
    # Destination account behaviour
    # ------------------------------------------------------------

    result["destination_balance_change_ratio"] = (
        result["destination_balance_change"].abs()
        / (result["oldbalanceDest"] + result["amount"] + 1)
    )

    # ------------------------------------------------------------
    # Balance anomaly indicators
    # ------------------------------------------------------------

    result["high_origin_balance_error"] = (
        result["origin_balance_error_abs"] > 1
    ).astype(int)

    result["high_destination_balance_error"] = (
        result["destination_balance_error_abs"] > 1
    ).astype(int)

    # ------------------------------------------------------------
    # Transaction characteristics
    # ------------------------------------------------------------

    result["is_large_transaction"] = (
        result["amount"] >= result["amount"].quantile(0.99)
    ).astype(int)

    result["is_zero_origin_before_withdrawal"] = (
        (result["origin_zero_balance_before"] == 1)
        & (result["amount"] > 0)
        & (result["is_transfer"] + result["is_cash_out"] > 0)
    ).astype(int)

    # ------------------------------------------------------------
    # Temporal features
    # ------------------------------------------------------------

    result["step_mod_24"] = result["step"] % 24

    result["is_late_step"] = (
        result["step"] >= result["step"].quantile(0.90)
    ).astype(int)

    # ------------------------------------------------------------
    # Interaction features
    # ------------------------------------------------------------

    result["transfer_or_cashout"] = (
        (result["is_transfer"] == 1)
        | (result["is_cash_out"] == 1)
    ).astype(int)

    result["large_transfer_or_cashout"] = (
        (result["is_large_transaction"] == 1)
        & (result["transfer_or_cashout"] == 1)
    ).astype(int)

    return result


def get_model_features(
    df: pd.DataFrame,
    include_flagged_fraud: bool = False,
) -> list[str]:
    """
    Return the recommended feature columns for modelling.

    The target variable is deliberately excluded.

    Account identifiers are excluded because their raw high-cardinality
    values are not suitable direct numerical model features.

    Parameters
    ----------
    df:
        Feature-engineered DataFrame.

    include_flagged_fraud:
        Whether to include the existing dataset fraud flag.

    Returns
    -------
    list[str]
        Model feature column names.
    """

    excluded = {
        "isFraud",
        "nameOrig",
        "nameDest",
        "type",
    }

    if not include_flagged_fraud:
        excluded.add("isFlaggedFraud")

    return [
        column
        for column in df.columns
        if column not in excluded
    ]
