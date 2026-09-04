# Phase 6 — Supervised Machine Learning

## Objective

Train and evaluate supervised classification models for fraud detection,
select an operating threshold, and investigate whether unusually strong
performance stems from leakage or problematic features.

## Status

**Complete** — matches the project-status table in the README.

## What Was Produced

- **Model definitions** — `src/machine_learning/models.py`:
  `create_logistic_regression`, `create_random_forest` (single canonical
  Random Forest configuration), `train_model`.

- **Evaluation** — `src/machine_learning/evaluation.py` using the shared
  metric helper `src/machine_learning/metrics.py`
  (`classification_metrics`): accuracy, precision, recall, F1-score,
  ROC-AUC.

- **Baseline training** — `scripts/train_baseline.py`: Logistic
  Regression and Random Forest baselines on a held-out split.

- **Held-out predictions** — `scripts/generate_random_forest_predictions.py`:
  writes actual-vs-probability pairs to
  `results/machine-learning/random-forest-predictions.csv`.

- **Threshold optimization** — `scripts/model_optimization.py` +
  `src/machine_learning/optimization.py`: evaluates the documented
  threshold grid (`default_thresholds`), computes per-threshold metrics,
  and selects the threshold maximizing F1-score. Output:
  `results/machine-learning/threshold-analysis.csv`.

- **Leakage analysis** — `scripts/leakage_analysis.py`: feature
  importance and correlation checks on the processed features. Output:
  `results/machine-learning/leakage-analysis-results.csv`.

- **Model comparison inputs** — verified results from this phase and
  Phase 7 feed the Phase 8 comparison report.

## Results

| Model | Accuracy | Precision | Recall | F1-score | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.967201 | 0.034137 | 0.894096 | 0.065762 | 0.984229 |
| Random Forest | 0.999995 | 0.998781 | 0.997565 | 0.998173 | 0.999087 |

Random Forest is the primary supervised model; Logistic Regression is
retained as the interpretable baseline. The exceptionally high Random
Forest performance must be interpreted carefully — it reflects the
synthetic PaySim generation process and is investigated for leakage in
this phase and caveated in the selection docs.

## How to Reproduce

```bash
python scripts/train_baseline.py [--max-rows N]
python scripts/generate_random_forest_predictions.py [--max-rows N]
python scripts/model_optimization.py
python scripts/leakage_analysis.py [--max-rows N]
```

## Related Documentation

- `docs/machine-learning/baseline-models.md`
- `docs/machine-learning/model-evaluation.md`
- `docs/machine-learning/leakage-analysis.md`
- `docs/machine-learning/model-selection.md` and
  `docs/machine-learning/final-model-selection.md` (selection results)
- `docs/phase-7/anomaly-detection.md` — the complementary next phase