# Phase 3 — Feature Engineering

## Objective

Add behavioural, ratio, and interaction features on top of the 24-column
processed dataset and define the exact feature list used by the models.

## Status

**Complete** — matches the project-status table in the README.

## What Was Produced

- **Feature-engineering module** — `src/feature_engineering/features.py`:

  - `engineer_features` — adds **12 behavioural features** to the
    24-column processed dataset, producing the **36-column
    feature-engineered dataset**. These include amount/balance ratios,
    balance-error flags, large-transaction and late-step indicators
    (computed once from full-column 0.99/0.90 quantiles), zero-origin
    withdrawal indicators, `step_mod_24` time features, and
    TRANSFER/CASH_OUT interaction indicators.
  - `get_model_features` — returns the **33 model features** by excluding
    the target `isFraud`, the categorical `type` column, the account
    identifiers, and (by default) the existing `isFlaggedFraud` flag.
  - Columns are assigned in place with no defensive copies, and
    thresholds/masks are computed once and reused — keeping memory and
    runtime bounded on the full dataset.

- **Consumers** — the 36-column frame and the 33-feature list are used by
  machine-learning preparation (Phase 5), baseline and final-model
  training (Phase 6/10), and the application's single-transaction
  inference service (Phase 10).

- **Tests** — `tests/test_feature_engineering.py` plus coverage inside the
  dataset-free end-to-end suite.

## Terminology

| Dataset | Columns |
|---|---|
| Processed (Phase 1) | 24 = 9 original + 15 engineered |
| Feature-engineered (this phase) | 36 = 24 + 12 behavioural features |
| Model features | 33 (excludes `isFraud`, `type`, `isFlaggedFraud` by default) |

## How to Reproduce

```bash
# No standalone CLI: the module is consumed by the ML entry points, e.g.
python scripts/train_baseline.py --max-rows 500000
python -m pytest tests/test_feature_engineering.py -q
```

## Related Documentation

- `docs/machine-learning/feature-engineering.md` — detailed engineering rationale
- `docs/data/processed-dataset.md` — the 24-column input layout
- `docs/phase-5/machine-learning-preparation.md` — the next phase