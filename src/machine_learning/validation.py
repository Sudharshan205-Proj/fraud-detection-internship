"""
Model validation and feature leakage analysis utilities.
"""

from __future__ import annotations

import pandas as pd
from sklearn.inspection import permutation_importance

from src.machine_learning.models import create_random_forest
from src.machine_learning.prepare import TARGET_COLUMN

IDENTIFIER_COLUMNS = [
    "nameOrig",
    "nameDest",
]

def identify_identifier_columns(
    df: pd.DataFrame,
) -> list[str]:
    """
    Identify account identifier columns that should not be used directly.
    """
    return [
        column
        for column in IDENTIFIER_COLUMNS
        if column in df.columns
    ]


def identify_suspicious_features(
    df: pd.DataFrame,
) -> list[str]:
    """
    Identify features that require leakage investigation.

    These are not automatically considered leakage. They are features
    whose relationship with the target or transaction outcome warrants
    further investigation.
    """
    known_risk_features = [
        "isFlaggedFraud",
        "origin_balance_error",
        "destination_balance_error",
        "origin_balance_error_abs",
        "destination_balance_error_abs",
        "origin_zero_balance_before",
        "origin_zero_balance_after",
        "destination_zero_balance_before",
        "destination_zero_balance_after",
        "amount_to_origin_balance",
        "amount_to_destination_balance",
    ]

    return [
        feature
        for feature in known_risk_features
        if feature in df.columns
    ]


def calculate_target_correlations(
    df: pd.DataFrame,
) -> pd.Series:
    """
    Calculate numerical feature correlations with the fraud target.
    """
    numeric_df = df.select_dtypes(include="number")

    if TARGET_COLUMN not in numeric_df.columns:
        raise ValueError(
            f"Target column '{TARGET_COLUMN}' must be numeric."
        )

    correlations = (
        numeric_df.corr()[TARGET_COLUMN]
        .drop(TARGET_COLUMN)
        .sort_values(key=abs, ascending=False)
    )

    return correlations


def train_validation_random_forest(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> tuple[object, pd.Series]:
    """
    Train a Random Forest and calculate permutation importance
    on the held-out test data.
    """
    model = create_random_forest()

    model.fit(X_train, y_train)

    importance = permutation_importance(
        model,
        X_test,
        y_test,
        scoring="f1",
        n_repeats=3,
        random_state=42,
        n_jobs=-1,
    )

    importance_series = pd.Series(
        importance.importances_mean,
        index=X_test.columns,
    ).sort_values(ascending=False)

    return model, importance_series
