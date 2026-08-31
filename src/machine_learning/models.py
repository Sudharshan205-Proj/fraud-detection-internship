"""
Baseline machine-learning models for fraud detection.
"""

from __future__ import annotations

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression


def create_logistic_regression(
    random_state: int = 42,
) -> LogisticRegression:
    """
    Create the baseline Logistic Regression classifier.
    """

    return LogisticRegression(
        max_iter=1000,
        random_state=random_state,
    )


def create_random_forest(
    random_state: int = 42,
) -> RandomForestClassifier:
    """
    Create the baseline Random Forest classifier.
    """

    return RandomForestClassifier(
        n_estimators=100,
        random_state=random_state,
        n_jobs=-1,
        class_weight="balanced",
    )
