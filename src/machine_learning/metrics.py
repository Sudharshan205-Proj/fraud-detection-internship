"""
Shared fraud-detection metric calculations.

Every model family (supervised classifiers, threshold analysis,
Isolation Forest, autoencoder) reports the same core metrics, so the
dictionary construction lives here instead of being duplicated.
"""

from __future__ import annotations

from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


def classification_metrics(
    y_true,
    y_pred,
    y_score,
    include_accuracy: bool = False,
) -> dict[str, float]:
    """Calculate the fraud-detection metrics shared by all model types.

    Parameters
    ----------
    y_true:
        Ground-truth binary labels.
    y_pred:
        Predicted binary labels.
    y_score:
        Continuous scores used for ROC-AUC (probabilities for
        classifiers, anomaly/reconstruction scores for detectors).
    include_accuracy:
        Whether to add the ``accuracy`` entry. Accuracy is excluded by
        default for anomaly detectors because it is misleading on
        highly imbalanced fraud data.

    Returns
    -------
    dict[str, float]
        Precision, recall, F1-score, ROC-AUC and (optionally) accuracy.
    """

    metrics = {
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1_score": f1_score(y_true, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_true, y_score),
    }

    if include_accuracy:
        metrics["accuracy"] = accuracy_score(y_true, y_pred)

    return metrics
