"""
Dataset-free end-to-end test for the threshold-analysis workflow.

Covers the Phase 6 chain on synthetic data, entirely under
``tmp_path``:

    processed frame
        -> generate_random_forest_predictions.generate_predictions
        -> predictions CSV
        -> model_optimization.analyze_predictions
        -> threshold-evaluation table + best threshold
"""

import pandas as pd
import pytest

from scripts.generate_random_forest_predictions import generate_predictions
from scripts.model_optimization import analyze_predictions
from src.machine_learning.optimization import default_thresholds
from tests.helpers import make_processed_frame

METRIC_COLUMNS = [
    "accuracy",
    "precision",
    "recall",
    "f1_score",
    "roc_auc",
]


def test_threshold_analysis_end_to_end(tmp_path):
    # ------------------------------------------------------------------
    # Stage 1: generate Random Forest predictions on a synthetic sample.
    # ------------------------------------------------------------------

    processed = make_processed_frame(80)

    prediction_path = tmp_path / "random-forest-predictions.csv"

    predictions = generate_predictions(processed, prediction_path)

    assert prediction_path.exists()
    assert list(predictions.columns) == ["actual", "probability"]
    assert len(predictions) == 16  # 20% held-out split of 80 rows.
    assert predictions["actual"].isin([0, 1]).all()
    assert predictions["probability"].between(0, 1).all()
    # Stratified split keeps both classes in the held-out predictions,
    # which ROC-AUC requires.
    assert predictions["actual"].nunique() == 2

    # ------------------------------------------------------------------
    # Stage 2: feed the predictions through threshold analysis.
    # ------------------------------------------------------------------

    results_path = tmp_path / "threshold-analysis.csv"

    results, best = analyze_predictions(
        prediction_path,
        output_path=results_path,
    )

    assert results_path.exists()

    saved = pd.read_csv(results_path)

    pd.testing.assert_frame_equal(results, saved)

    # Full threshold grid at the documented default resolution.
    assert list(results["threshold"]) == default_thresholds()
    assert len(results) == len(default_thresholds())

    assert results.columns[0] == "threshold"
    assert set(results.columns) == {"threshold", *METRIC_COLUMNS}

    for column in METRIC_COLUMNS:
        assert results[column].between(0, 1).all()

    # Best-threshold row is the F1-score argmax of the table.
    assert best["f1_score"] == results["f1_score"].max()
    assert best["threshold"] == results.loc[
        results["f1_score"].idxmax(),
        "threshold",
    ]

    # The selected row is present verbatim in the saved table.
    best_reloaded = saved[saved["threshold"] == best["threshold"]].iloc[0]
    assert best_reloaded["f1_score"] == best["f1_score"]


def test_analyze_predictions_requires_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        analyze_predictions(tmp_path / "missing-predictions.csv")


def test_analyze_predictions_validates_columns(tmp_path):
    bad_path = tmp_path / "bad-predictions.csv"
    pd.DataFrame({"actual": [0, 1]}).to_csv(bad_path, index=False)

    with pytest.raises(ValueError, match="Missing required columns"):
        analyze_predictions(bad_path)
