"""
Generate held-out Random Forest predictions for Phase 6 threshold analysis.
"""

import argparse
from pathlib import Path

import pandas as pd

from src.data_processing.process_data import load_processed_dataset
from src.machine_learning.models import create_random_forest
from src.machine_learning.prepare import (
    prepare_categorical_features,
    split_features_target,
    train_test_split_data,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]

OUTPUT_PATH = (
    PROJECT_ROOT
    / "results"
    / "machine-learning"
    / "random-forest-predictions.csv"
)

TARGET_COLUMN = "isFraud"


def generate_predictions(
    df: pd.DataFrame,
    output_path: str | Path,
    test_size: float = 0.2,
) -> pd.DataFrame:
    """
    Train a Random Forest and write held-out predictions to CSV.

    The predictions CSV contains the ``actual`` fraud label and the
    ``probability`` of fraud for each held-out transaction.

    Parameters
    ----------
    df:
        Processed PaySim dataset (24 columns).
    output_path:
        Destination for the predictions CSV.
    test_size:
        Held-out fraction used for the stratified split.

    Returns
    -------
    pandas.DataFrame
        The saved predictions frame (``actual``, ``probability``).
    """

    X, y = split_features_target(df)

    X = prepare_categorical_features(X)

    X_train, X_test, y_train, y_test = train_test_split_data(
        X,
        y,
        test_size=test_size,
    )

    model = create_random_forest()

    print("Training Random Forest...")

    model.fit(X_train, y_train)

    probabilities = model.predict_proba(X_test)[:, 1]

    predictions = pd.DataFrame(
        {
            "actual": y_test.to_numpy(),
            "probability": probabilities,
        }
    )

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    predictions.to_csv(
        output_path,
        index=False,
    )

    return predictions


def main(max_rows: int | None = None) -> None:
    print("Loading processed dataset...")

    df = load_processed_dataset(max_rows=max_rows)

    if max_rows is not None:
        print(f"Sample mode active: using at most {max_rows:,} rows.")

    predictions = generate_predictions(
        df,
        OUTPUT_PATH,
    )

    print("Prediction generation complete.")
    print(f"Rows: {len(predictions):,}")
    print(
        "Fraudulent test observations:",
        int(predictions["actual"].sum()),
    )
    print(
        "Saved to:",
        OUTPUT_PATH.relative_to(PROJECT_ROOT),
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Train a Random Forest and save held-out fraud probabilities "
            "for threshold analysis."
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
