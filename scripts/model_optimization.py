"""
Phase 6: Model optimization and threshold analysis.

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
    / "results"
    / "machine-learning"
    / "threshold-analysis.csv"
)

PREDICTION_PATH = (
    PROJECT_ROOT
    / "results"
    / "machine-learning"
    / "random-forest-predictions.csv"
)

REQUIRED_COLUMNS = {
    "actual",
    "probability",
}


def analyze_predictions(
    prediction_path: str | Path,
    output_path: str | Path | None = None,
) -> tuple[pd.DataFrame, pd.Series]:
    """
    Run threshold analysis over saved Random Forest predictions.

    Parameters
    ----------
    prediction_path:
        CSV containing the ``actual`` fraud labels and ``probability``
        scores produced by ``generate_random_forest_predictions``.
    output_path:
        Optional destination for the full threshold-evaluation table.

    Returns
    -------
    tuple[pandas.DataFrame, pandas.Series]
        The threshold-evaluation table and the best-threshold row
        (selected by F1-score).
    """

    prediction_path = Path(prediction_path)

    if not prediction_path.exists():
        raise FileNotFoundError(
            "Random Forest prediction file was not found: "
            f"{prediction_path}"
        )

    predictions = pd.read_csv(prediction_path)

    missing = REQUIRED_COLUMNS - set(predictions.columns)

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

    if output_path is not None:
        output_path = Path(output_path)
        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        results.to_csv(
            output_path,
            index=False,
        )

    return results, best


def main() -> None:
    """
    Run threshold analysis using the saved model predictions.
    """

    results, best = analyze_predictions(
        PREDICTION_PATH,
        output_path=RESULTS_PATH,
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
