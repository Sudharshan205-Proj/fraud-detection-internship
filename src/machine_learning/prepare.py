"""
Machine-learning data preparation utilities.

This module handles train/test splitting, categorical encoding,
feature preparation, scaling, and class-imbalance handling.
"""

from __future__ import annotations

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

TARGET_COLUMN = "isFraud"

IDENTIFIER_COLUMNS = ["nameOrig", "nameDest"]

CATEGORICAL_COLUMNS = ["type"]


def split_features_target(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.Series]:
    """
    Separate predictors from the fraud target.
    """

    if TARGET_COLUMN not in df.columns:
        raise ValueError(
            f"Target column '{TARGET_COLUMN}' not found."
        )

    X = df.drop(columns=[TARGET_COLUMN])
    y = df[TARGET_COLUMN]

    return X, y


def prepare_categorical_features(
    X: pd.DataFrame,
) -> pd.DataFrame:
    """
    Remove high-cardinality identifiers and one-hot encode the
    categorical transaction-type variable.

    ``pd.get_dummies`` already returns a new frame, so no defensive
    copy is made first.
    """

    present_identifiers = [
        column for column in IDENTIFIER_COLUMNS if column in X.columns
    ]

    if present_identifiers:
        X = X.drop(columns=present_identifiers)

    present_categorical = [
        column for column in CATEGORICAL_COLUMNS if column in X.columns
    ]

    if present_categorical:
        X = pd.get_dummies(
            X,
            columns=present_categorical,
            drop_first=False,
            dtype=int,
        )

    return X


def train_test_split_data(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float = 0.2,
    random_state: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Perform a stratified train/test split.
    """

    return train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )


def scale_features(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, StandardScaler]:
    """
    Scale numerical features using statistics learned only
    from the training set.
    """

    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    X_train_scaled = pd.DataFrame(
        X_train_scaled,
        columns=X_train.columns,
        index=X_train.index,
    )

    X_test_scaled = pd.DataFrame(
        X_test_scaled,
        columns=X_test.columns,
        index=X_test.index,
    )

    return X_train_scaled, X_test_scaled, scaler


def apply_smote(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    random_state: int = 42,
) -> tuple[pd.DataFrame, pd.Series]:
    """
    Apply SMOTE to the training data only.

    The number of SMOTE neighbours is adapted to the available
    minority-class samples so that small test datasets can still
    be processed safely.
    """
    from imblearn.over_sampling import SMOTE

    minority_count = y_train.value_counts().min()

    if minority_count < 2:
        raise ValueError(
            "SMOTE requires at least 2 samples in the minority class."
        )

    k_neighbors = min(5, minority_count - 1)

    smote = SMOTE(
        random_state=random_state,
        k_neighbors=k_neighbors,
    )

    X_resampled, y_resampled = smote.fit_resample(
        X_train,
        y_train,
    )

    return X_resampled, y_resampled
