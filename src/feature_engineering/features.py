"""
Feature engineering utilities for the fraud detection project.

Terminology
-----------
* The processed PaySim dataset has 24 columns (9 original columns
  retained + 15 engineered features).
* This module adds 12 further behavioural features, producing the
  36-column feature-engineered dataset.
* :func:`get_model_features` selects the 33 model features by
  excluding the target ``isFraud``, the existing ``isFlaggedFraud``
  flag (by default), and the categorical ``type`` column.

The module creates the additional behavioural and transaction-level
features from the processed PaySim dataset.
"""

from __future__ import annotations

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

# Features created by the processing pipeline that this stage builds on.
REQUIRED_DERIVED_COLUMNS = [
    "origin_balance_change",
    "destination_balance_change",
    "origin_balance_error_abs",
    "destination_balance_error_abs",
    "origin_zero_balance_before",
    "is_transfer",
    "is_cash_out",
    "log_amount",
]


def _validate_input_columns(df: pd.DataFrame) -> None:
    missing_columns = [
        column
        for column in REQUIRED_COLUMNS + REQUIRED_DERIVED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing required columns: "
            f"{missing_columns}. Process the raw data with "
            "src.data_processing.process_data first."
        )


def engineer_features(
    df: pd.DataFrame,
    large_amount_threshold: float | None = None,
    late_step_threshold: float | None = None,
) -> pd.DataFrame:
    """
    Create additional fraud-detection features.

    Adds 12 behavioural features to the 24-column processed dataset,
    producing the 36-column feature-engineered dataset. Columns are
    assigned in place on the supplied frame (no defensive copy).

    Parameters
    ----------
    df:
        Processed PaySim DataFrame (24 columns).
    large_amount_threshold:
        Optional pre-computed 0.99 amount quantile. When omitted it is
        derived from ``df``; pass the persisted training quantile when
        engineering a single transaction so inference matches training.
    late_step_threshold:
        Optional pre-computed 0.90 step quantile. When omitted it is
        derived from ``df``; pass the persisted training quantile when
        engineering a single transaction so inference matches training.

    Returns
    -------
    pd.DataFrame
        The same frame with the 12 engineered columns appended.
    """

    _validate_input_columns(df)

    # ------------------------------------------------------------
    # Transaction amount features
    # ------------------------------------------------------------

    # ``log_amount`` was already computed by the processing pipeline;
    # reuse it instead of recomputing the log over the full dataset.
    df["amount_log_ratio"] = df["log_amount"]

    df["amount_to_origin_balance"] = (
        df["amount"]
        / (df["oldbalanceOrg"] + 1)
    )

    df["amount_to_destination_balance"] = (
        df["amount"]
        / (df["oldbalanceDest"] + 1)
    )

    # ------------------------------------------------------------
    # Origin account behaviour
    # ------------------------------------------------------------

    df["origin_balance_change_ratio"] = (
        df["origin_balance_change"].abs()
        / (df["oldbalanceOrg"] + 1)
    )

    df["origin_balance_utilization"] = (
        df["amount"]
        / (df["oldbalanceOrg"] + df["amount"] + 1)
    )

    # ------------------------------------------------------------
    # Destination account behaviour
    # ------------------------------------------------------------

    df["destination_balance_change_ratio"] = (
        df["destination_balance_change"].abs()
        / (df["oldbalanceDest"] + df["amount"] + 1)
    )

    # ------------------------------------------------------------
    # Balance anomaly indicators
    # ------------------------------------------------------------

    df["high_origin_balance_error"] = (
        df["origin_balance_error_abs"] > 1
    ).astype(int)

    df["high_destination_balance_error"] = (
        df["destination_balance_error_abs"] > 1
    ).astype(int)

    # ------------------------------------------------------------
    # Transaction characteristics
    # ------------------------------------------------------------

    # Full-column thresholds computed once and reused below (or supplied
    # by the caller, e.g. the application using persisted training values).
    if large_amount_threshold is None:
        large_amount_threshold = df["amount"].quantile(0.99)

    if late_step_threshold is None:
        late_step_threshold = df["step"].quantile(0.90)

    # TRANSFER/CASH_OUT activity reused by several indicators.
    withdrawal_activity = (
        (df["is_transfer"] == 1)
        | (df["is_cash_out"] == 1)
    )

    df["is_large_transaction"] = (
        df["amount"] >= large_amount_threshold
    ).astype(int)

    df["is_zero_origin_before_withdrawal"] = (
        (df["origin_zero_balance_before"] == 1)
        & (df["amount"] > 0)
        & withdrawal_activity
    ).astype(int)

    # ------------------------------------------------------------
    # Temporal features
    # ------------------------------------------------------------

    df["step_mod_24"] = df["step"] % 24

    df["is_late_step"] = (
        df["step"] >= late_step_threshold
    ).astype(int)

    # ------------------------------------------------------------
    # Interaction features
    # ------------------------------------------------------------

    df["transfer_or_cashout"] = withdrawal_activity.astype(int)

    df["large_transfer_or_cashout"] = (
        (df["is_large_transaction"] == 1)
        & (df["transfer_or_cashout"] == 1)
    ).astype(int)

    return df


def get_model_features(
    df: pd.DataFrame,
    include_flagged_fraud: bool = False,
) -> list[str]:
    """
    Return the recommended feature columns for modelling.

    The target variable is deliberately excluded.

    Account identifiers are excluded because their raw high-cardinality
    values are not suitable direct numerical model features.

    On the 36-column feature-engineered dataset this returns the
    33 model features (``isFraud``, ``type`` and, by default,
    ``isFlaggedFraud`` are excluded).

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
