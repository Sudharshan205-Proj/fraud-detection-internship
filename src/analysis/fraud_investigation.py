"""
Phase 9 - Fraud investigation support.

Provides transaction-level investigation outputs using the
selected Random Forest model and model feature importance.
"""

import argparse
from pathlib import Path

import pandas as pd

from src.data_processing.process_data import load_processed_dataset
from src.machine_learning.explainability import get_feature_importance
from src.machine_learning.models import create_random_forest
from src.machine_learning.prepare import prepare_categorical_features

PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = (
    PROJECT_ROOT
    / "docs"
    / "machine-learning"
    / "explainability"
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

    # Reuse the shared categorical preparation (identifier removal +
    # one-hot encoding of the transaction type).
    X = prepare_categorical_features(X)

    return X, y


def train_investigation_model(X, y):
    """
    Train the Random Forest model used for investigation.
    """

    model = create_random_forest()

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


def main(max_rows: int | None = None) -> None:
    print("Loading processed dataset...")

    df = load_processed_dataset(max_rows=max_rows)

    if max_rows is not None:
        print(f"Sample mode active: using at most {max_rows:,} rows.")

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
    parser = argparse.ArgumentParser(
        description=(
            "Generate a transaction-level fraud-investigation report "
            "using the selected Random Forest model."
        ),
    )
    parser.add_argument(
        "--max-rows",
        type=int,
        default=None,
        metavar="N",
        help="Optional row cap for fast sample-mode runs (default: full dataset).",
    )
    args = parser.parse_args()

    main(max_rows=args.max_rows)
