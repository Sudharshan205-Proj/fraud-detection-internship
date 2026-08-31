"""
Phase 7: Model optimization and threshold analysis.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


def calculate_metrics(
    y_true: pd.Series,
    probabilities: np.ndarray,
    threshold: float = 0.5,
) -> dict[str, float]:
    """
    Calculate fraud-detection metrics for a probability threshold.
    """

    predictions = (probabilities >= threshold).astype(int)

    return {
        "threshold": threshold,
        "accuracy": accuracy_score(y_true, predictions),
        "precision": precision_score(
            y_true,
            predictions,
            zero_division=0,
        ),
        "recall": recall_score(
            y_true,
            predictions,
            zero_division=0,
        ),
        "f1_score": f1_score(
            y_true,
            predictions,
            zero_division=0,
        ),
        "roc_auc": roc_auc_score(
            y_true,
            probabilities,
        ),
    }


def evaluate_thresholds(
    y_true: pd.Series,
    probabilities: np.ndarray,
    thresholds: list[float] | None = None,
) -> pd.DataFrame:
    """
    Evaluate a model over multiple classification thresholds.
    """

    if thresholds is None:
        thresholds = [
            0.10,
            0.15,
            0.20,
            0.25,
            0.30,
            0.35,
            0.40,
            0.45,
            0.50,
            0.55,
            0.60,
            0.65,
            0.70,
            0.75,
            0.80,
            0.85,
            0.90,
            0.95,
        ]

    results = [
        calculate_metrics(
            y_true,
            probabilities,
            threshold,
        )
        for threshold in thresholds
    ]

    return pd.DataFrame(results)


def select_best_threshold(
    threshold_results: pd.DataFrame,
    metric: str = "f1_score",
) -> pd.Series:
    """
    Select the threshold producing the highest value for the
    requested evaluation metric.
    """

    if metric not in threshold_results.columns:
        raise ValueError(
            f"Metric '{metric}' is not present in threshold results."
        )

    best_index = threshold_results[metric].idxmax()

    return threshold_results.loc[best_index]


def compare_model_scores(
    results: dict[str, dict[str, float]],
) -> pd.DataFrame:
    """
    Convert model evaluation results into a comparison table.
    """

    return pd.DataFrame(results).T
