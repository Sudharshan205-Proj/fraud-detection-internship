"""
Phase 7: Model optimization and threshold analysis.

This script evaluates classification thresholds for the Random Forest
model and identifies the threshold that provides the strongest F1-score.
"""

from pathlib import Path

import pandas as pd

from src.machine_learning.optimization import (
    evaluate_thresholds,
    select_best_threshold,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RESULTS_PATH = (
    PROJECT_ROOT
    / "docs"
    / "machine-learning"
    / "threshold-analysis.csv"
)


def main() -> None:
    """
    Run threshold analysis using the saved model predictions.
    """

    prediction_path = (
        PROJECT_ROOT
        / "docs"
        / "machine-learning"
        / "random-forest-predictions.csv"
    )

    if not prediction_path.exists():
        raise FileNotFoundError(
            "Random Forest prediction file was not found: "
            f"{prediction_path}"
        )

    predictions = pd.read_csv(prediction_path)

    required_columns = {
        "actual",
        "probability",
    }

    missing = required_columns - set(predictions.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    y_true = predictions["actual"]
    probabilities = predictions["probability"].to_numpy()

    results = evaluate_thresholds(
        y_true,
        probabilities,
    )

    best = select_best_threshold(
        results,
        metric="f1_score",
    )

    RESULTS_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    results.to_csv(
        RESULTS_PATH,
        index=False,
    )

    print("Threshold analysis complete.")
    print()
    print("Best threshold based on F1-score:")
    print(best.to_string())
    print()
    print(
        "Results saved to:",
        RESULTS_PATH.relative_to(PROJECT_ROOT),
    )


if __name__ == "__main__":
    main()
