"""
Phase 9 - Fraud investigation support.

Provides transaction-level investigation outputs using the
selected Random Forest model and model feature importance.
"""

from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier

DATA_PATH = Path(
    "data/processed/paysim_processed.csv"
)

OUTPUT_DIR = Path(
    "docs/machine-learning/explainability"
)


def prepare_features(df):
    """
    Prepare transaction features for the Random Forest model.

    Returns:
        X: model-ready feature DataFrame
        y: target Series
    """

    target = "isFraud"

    if target not in df.columns:
        raise ValueError(
            f"Required target column '{target}' is missing."
        )

    X = df.drop(columns=[target])
    y = df[target]

    if "type" in X.columns:
        X = pd.get_dummies(
            X,
            columns=["type"],
            dtype=int,
        )

    return X, y


def train_investigation_model(X, y):
    """
    Train the Random Forest model used for investigation.
    """

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        n_jobs=-1,
        class_weight="balanced",
    )

    model.fit(X, y)

    return model


def create_investigation_report(
    model,
    X,
    original_df,
    feature_importance,
    top_n=10,
):
    """
    Create transaction-level investigation information.

    Each transaction receives:
    - predicted fraud label
    - fraud probability
    - investigation priority
    - top globally important features

    The output is intended to support analyst investigation,
    not to establish that a transaction is fraudulent.
    """

    predictions = model.predict(X)

    probabilities = model.predict_proba(X)

    fraud_probability = probabilities[:, 1]

    report = original_df.copy()

    report["predicted_fraud"] = predictions
    report["fraud_probability"] = fraud_probability

    report["investigation_priority"] = pd.cut(
        fraud_probability,
        bins=[
            -0.01,
            0.25,
            0.50,
            0.75,
            1.00,
        ],
        labels=[
            "Low",
            "Moderate",
            "High",
            "Critical",
        ],
    )

    important_features = feature_importance.head(
        top_n
    )["feature"].tolist()

    available_features = [
        feature
        for feature in important_features
        if feature in X.columns
    ]

    report["important_features_available"] = (
        ", ".join(available_features)
    )

    report = report.sort_values(
        by="fraud_probability",
        ascending=False,
    )

    return report


def save_investigation_report(
    report,
    output_path,
):
    """
    Save the investigation report as CSV.
    """

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    report.to_csv(
        output_path,
        index=False,
    )


def main():
    print("Loading processed dataset...")

    df = pd.read_csv(DATA_PATH)

    print("Rows:", len(df))
    print("Columns:", len(df.columns))

    print("\nPreparing model features...")

    X, y = prepare_features(df)

    print("Feature matrix:", X.shape)

    print("\nTraining Random Forest...")

    model = train_investigation_model(
        X,
        y,
    )

    print("Model trained successfully.")

    from src.machine_learning.explainability import (
        get_feature_importance,
    )

    feature_importance = get_feature_importance(
        model,
        X.columns,
    )

    print("\nCreating investigation report...")

    report = create_investigation_report(
        model=model,
        X=X,
        original_df=df,
        feature_importance=feature_importance,
        top_n=10,
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        OUTPUT_DIR
        / "fraud-investigation-report.csv"
    )

    save_investigation_report(
        report,
        output_path,
    )

    print("\nInvestigation report saved:")
    print(output_path)

    print("\nTop 10 highest-risk transactions:")
    print(
        report[
            [
                "fraud_probability",
                "predicted_fraud",
                "investigation_priority",
            ]
        ]
        .head(10)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()
