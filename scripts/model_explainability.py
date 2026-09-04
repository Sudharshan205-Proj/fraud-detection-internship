"""
Phase 9 - Random Forest model explainability analysis.
"""

import argparse
from pathlib import Path

import pandas as pd

from src.data_processing.process_data import load_processed_dataset
from src.machine_learning.explainability import (
    get_feature_importance,
    plot_feature_importance,
    save_feature_importance,
)
from src.machine_learning.models import create_random_forest

PROJECT_ROOT = Path(__file__).resolve().parents[1]

OUTPUT_DIR = (
    PROJECT_ROOT
    / "docs"
    / "machine-learning"
    / "explainability"
)

IDENTIFIER_COLUMNS = [
    "nameOrig",
    "nameDest",
]


def prepare_model_data(df: pd.DataFrame):
    """
    Split the target and prepare a model-ready feature matrix.

    Account identifiers are removed if still present and the
    categorical ``type`` variable is one-hot encoded.
    """
    target = "isFraud"

    if target not in df.columns:
        raise ValueError(
            f"Required target column '{target}' is missing."
        )

    X = df.drop(columns=[target])
    y = df[target]

    present_identifiers = [
        column for column in IDENTIFIER_COLUMNS if column in X.columns
    ]

    if present_identifiers:
        X = X.drop(
            columns=present_identifiers,
            errors="ignore",
        )

    if "type" in X.columns:
        X = pd.get_dummies(
            X,
            columns=["type"],
            dtype=int,
        )

    return X, y


def main(max_rows: int | None = None) -> None:
    print("Loading processed dataset...")

    df = load_processed_dataset(max_rows=max_rows)

    if max_rows is not None:
        print(f"Sample mode active: using at most {max_rows:,} rows.")

    print("Rows:", len(df))
    print("Columns:", len(df.columns))

    X, y = prepare_model_data(df)

    print("Prepared features:", X.shape[1])

    print("\nTraining Random Forest for explainability...")

    model = create_random_forest()

    model.fit(X, y)

    print("Model trained successfully.")

    feature_importance = get_feature_importance(
        model,
        X.columns,
    )

    print("\nTop 15 Features")
    print("=" * 60)
    print(
        feature_importance.head(15).to_string(
            index=False
        )
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    csv_path = (
        OUTPUT_DIR
        / "random-forest-feature-importance.csv"
    )

    image_path = (
        OUTPUT_DIR
        / "random-forest-feature-importance.png"
    )

    save_feature_importance(
        feature_importance,
        csv_path,
    )

    plot_feature_importance(
        feature_importance,
        image_path,
        top_n=15,
    )

    print("\nFeature importance saved:")
    print(csv_path)

    print("\nFeature importance chart saved:")
    print(image_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Train the Random Forest and generate feature-importance "
            "outputs for model explainability."
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
