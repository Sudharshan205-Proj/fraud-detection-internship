"""
Phase 6: Feature importance and leakage analysis.

This script investigates the processed PaySim features to determine
whether unusually strong model performance may be associated with
potentially problematic features.
"""

from pathlib import Path

import pandas as pd  # noqa: F401

from src.machine_learning.validation import (
    calculate_target_correlations,
    identify_identifier_columns,
    identify_suspicious_features,
    load_processed_dataset,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = PROJECT_ROOT / "data" / "processed" / "paysim_processed.csv"

OUTPUT_PATH = (
    PROJECT_ROOT
    / "docs"
    / "machine-learning"
    / "leakage-analysis-results.csv"
)


def main() -> None:
    print("Loading processed dataset...")

    df = load_processed_dataset(DATA_PATH)

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
        f"\nResults saved to: "
        f"{OUTPUT_PATH.relative_to(PROJECT_ROOT)}"
    )


if __name__ == "__main__":
    main()
