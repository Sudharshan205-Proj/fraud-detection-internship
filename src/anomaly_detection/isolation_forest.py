from __future__ import annotations

import pandas as pd
from sklearn.ensemble import IsolationForest

from src.machine_learning.metrics import classification_metrics


def create_isolation_forest(
    contamination: float = 0.01,
    random_state: int = 42,
) -> IsolationForest:
    """
    Create an Isolation Forest anomaly-detection model.
    """
    return IsolationForest(
        n_estimators=200,
        contamination=contamination,
        random_state=random_state,
        n_jobs=-1,
    )


def fit_isolation_forest(
    model: IsolationForest,
    X_train,
) -> IsolationForest:
    """
    Train Isolation Forest on the supplied feature matrix.
    """
    model.fit(X_train)
    return model


def predict_anomalies(
    model: IsolationForest,
    X,
) -> tuple:
    """
    Return anomaly predictions and anomaly scores.

    Isolation Forest:
        1  = normal
       -1  = anomaly
    """
    predictions = model.predict(X)
    scores = -model.decision_function(X)

    return predictions, scores


def convert_predictions_to_binary(
    predictions,
):
    """
    Convert Isolation Forest output:

        -1 -> 1 (anomaly)
         1 -> 0 (normal)
    """
    return (predictions == -1).astype(int)


def evaluate_isolation_forest(
    y_true,
    y_pred,
    anomaly_scores,
) -> dict:
    """
    Evaluate Isolation Forest using fraud-detection metrics.

    The negative decision-function values are used as continuous
    anomaly scores for ROC-AUC.
    """
    return classification_metrics(
        y_true,
        y_pred,
        anomaly_scores,
        include_accuracy=False,
    )


def results_to_dataframe(
    X,
    predictions,
    anomaly_scores,
) -> pd.DataFrame:
    """
    Create a dataframe containing anomaly predictions and scores.
    """
    results = X.copy()

    results["anomaly_prediction"] = predictions
    results["anomaly_score"] = anomaly_scores

    return results
