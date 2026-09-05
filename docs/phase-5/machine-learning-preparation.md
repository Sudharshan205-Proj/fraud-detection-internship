# Phase 5 — Machine Learning Preparation

## Objective

Turn the feature-engineered 36-column dataset into model-ready inputs
(split, encoded, scaled, optionally resampled) without introducing data
leakage.

## Status

**Complete** — matches the project-status table in the README.

## What Was Produced

- **Preparation module** — `src/machine_learning/prepare.py`:

  - `split_features_target` — separates features from the `isFraud` target
  - `prepare_categorical_features` — one-hot encodes the `type` column
  - `train_test_split_data` — stratified train/test split so the rare
    fraud class is represented in both partitions
  - `scale_features` — feature scaling for models that require it
  - `apply_smote` — SMOTE resampling of the minority class

- **Validation module** — `src/machine_learning/validation.py`:

  - `identify_identifier_columns` / `identify_suspicious_features` /
    `calculate_target_correlations` — pre-modelling feature scrutiny

- **Leakage rules enforced in this phase:**

  - The train/test split happens **before** SMOTE and before any
    scaling fit, so the test set is never touched by training-time
    transformations.
  - SMOTE is applied only to training data.
  - Account identifiers are never used as features.

- **Tests** — `tests/test_machine_learning.py` and the dataset-free
  end-to-end suite, which verifies the split keeps both classes in
  train and test.

## How to Reproduce

```bash
# Preparation is exercised by the model entry points, e.g.
python scripts/train_baseline.py --max-rows 500000
python -m pytest tests/test_machine_learning.py -q
```

## Related Documentation

- `docs/machine-learning/ml-preparation.md` — detailed preparation
  rationale, including SMOTE
- `docs/phase-3/feature-engineering.md` — the 33-feature input
- `docs/phase-6/supervised-machine-learning.md` — the next phase