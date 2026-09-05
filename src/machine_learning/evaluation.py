"""
Supervised model evaluation helpers.

Provides a single entry point for scoring fitted binary classifiers
with the fraud-detection metric set shared across the project.
"""

from src.machine_learning.metrics import classification_metrics


def evaluate_model(model, X_test, y_test):
    """
    Evaluate a binary classification model.

    Returns a dictionary containing the main fraud-detection metrics:
    accuracy, precision, recall, F1-score and ROC-AUC.
    """
    y_pred = model.predict(X_test)

    if hasattr(model, "predict_proba"):
        y_score = model.predict_proba(X_test)[:, 1]
    else:
        y_score = model.decision_function(X_test)

    return classification_metrics(
        y_test,
        y_pred,
        y_score,
        include_accuracy=True,
    )
