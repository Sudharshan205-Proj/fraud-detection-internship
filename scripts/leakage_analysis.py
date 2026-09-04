"""
Phase 6: Feature importance and leakage analysis.

This script investigates the processed PaySim features to determine
whether unusually strong model performance may be associated with
potentially problematic features.
"""

import argparse
from pathlib import Path

from src.data_processing.process_data import load_processed_dataset
from src.machine_learning.validation import (
    calculate_target_correlations,
    identify_identifier_columns,
    identify_suspicious_features,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]

OUTPUT_PATH = (
    PROJECT_ROOT
    / "results"
    / "machine-learning"
    / "leakage-analysis-results.csv"
)


def main(max_rows: int | None = None) -> None:
    print("Loading processed dataset...")

    df = load_processed_dataset(max_rows=max_rows)

    if max_rows is not None:
        print(f"Sample mode active: using at most {max_rows:,} rows.")

    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    print("\nIdentifier columns:")
    identifiers = identify_identifier_columns(df)

    if identifiers:
        for column in identifiers:
            print(f"- {column}")
    else:
        print("- None")

    print("\nFeatures requiring leakage assessment:")
    suspicious_features = identify_suspicious_features(df)

    for feature in suspicious_features:
        print(f"- {feature}")

    print("\nTarget correlations:")

    correlations = calculate_target_correlations(df)

    print(correlations.to_string())

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    correlations.rename("correlation_with_isFraud").to_csv(
        OUTPUT_PATH,
        header=True,
    )

    print(
        "\nResults saved to: "
        f"{OUTPUT_PATH.relative_to(PROJECT_ROOT)}"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Investigate feature correlations and leakage risk in the "
            "processed PaySim dataset."
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
