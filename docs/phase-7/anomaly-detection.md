# Phase 7 — Anomaly Detection

## Objective

Investigate unsupervised anomaly-detection approaches as complementary
methods to the supervised classifiers: Isolation Forest and an
autoencoder. Both are evaluated against the known PaySim fraud labels
for post-hoc analytical validation only.

## Status

**Complete** — matches the project-status table in the README.

## What Was Produced

- **Anomaly pipeline** — `src/anomaly_detection/pipeline.py`:

  - `prepare_features` — builds a single numeric feature matrix from the
    24-column processed dataset (no redundant DataFrame copies)
  - `split_and_scale` — train/test split and scaling before any training
  - `run_isolation_forest` — Isolation Forest with 200 trees, random
    state 42, contamination 0.01; produces anomaly scores and binary
    predictions
  - `run_autoencoder` — Keras autoencoder
    (Input → Encoder → Latent → Decoder → Output) trained on legitimate
    training transactions only; anomaly classification uses the
    99th-percentile reconstruction-error threshold; `verbose` parameter
    for quiet test runs

- **Helpers** — `src/anomaly_detection/isolation_forest.py` and
  `src/anomaly_detection/autoencoder.py`.

- **Tests** — `tests/anomaly_detection/` including dataset-free
  end-to-end tests that train both detectors on a synthetic processed
  frame and check the four-metric contract.

## Results

| Model | Precision | Recall | F1-score | ROC-AUC |
|---|---:|---:|---:|---:|
| Isolation Forest | 0.035260 | 0.270237 | 0.062381 | 0.893615 |
| Autoencoder | 0.089292 | 0.742544 | 0.159415 | 0.941359 |

Interpretation: both approaches detect fraud at lower precision than the
supervised Random Forest, but demonstrate genuine anomaly-detection
capability; the autoencoder achieves substantially higher recall. An
anomaly score is not proof of fraud — labels are used only for post-hoc
evaluation.

## How to Reproduce

```bash
python -m src.anomaly_detection.pipeline [--max-rows N]
```

## Related Documentation

- `docs/anomaly-detection/anomaly-detection-report.md` — full report
  including leakage considerations and limitations
- `docs/phase-6/supervised-machine-learning.md` — the supervised approaches
- `docs/phase-8/model-comparison.md` — how the four models compare