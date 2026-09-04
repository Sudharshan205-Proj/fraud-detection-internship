"""
Phase 6: Model optimization and threshold analysis.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.machine_learning.metrics import classification_metrics


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
        **classification_metrics(
            y_true,
            predictions,
            probabilities,
            include_accuracy=True,
        ),
    }


def default_thresholds() -> list[float]:
    """
    Return the default threshold grid from 0.10 to 0.95 inclusive.
    """

    return [
        float(threshold)
        for threshold in np.round(
            np.arange(0.10, 0.951, 0.05),
            2,
        )
    ]


def evaluate_thresholds(
    y_true: pd.Series,
    probabilities: np.ndarray,
    thresholds: list[float] | None = None,
) -> pd.DataFrame:
    """
    Evaluate a model over multiple classification thresholds.
    """

    if thresholds is None:
        thresholds = default_thresholds()

    results = [
        calculate_metrics(y_true, probabilities, threshold)
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
