"""
Model factories for the supervised classification baselines.

Both the Logistic Regression baseline and the selected Random Forest
use balanced class weighting because the PaySim fraud target is
extremely imbalanced.
"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression


def create_logistic_regression(random_state: int = 42):
    """
    Create the baseline Logistic Regression model.
    """
    return LogisticRegression(
        random_state=random_state,
        max_iter=1000,
        class_weight="balanced",
    )


def create_random_forest(random_state: int = 42):
    """
    Create the baseline Random Forest classifier.
    """
    return RandomForestClassifier(
        n_estimators=100,
        random_state=random_state,
        n_jobs=-1,
        class_weight="balanced",
    )


def train_model(model, X_train, y_train):
    """
    Train a machine-learning model using the supplied training data.
    """
    model.fit(X_train, y_train)
    return model
