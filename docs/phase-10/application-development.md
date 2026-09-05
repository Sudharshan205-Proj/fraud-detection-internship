# Phase 10 — Application Development

## Objective

Build a lightweight internship-level interface that scores individual
transactions with the selected Random Forest model and presents the
result as an analyst-facing fraud assessment with investigation
priority.

## Status

**Complete** — matches the project-status table in the README. The
model-training, inference service, and Streamlit UI are implemented,
tested, and runnable.

## What Was Produced

- **`app/model_service.py`** — `FraudModelService`:

  - loads `models/random_forest_model.joblib` and
    `models/model_features.json`
  - validates that the model's expected feature count matches the
    persisted 33-feature schema
  - rebuilds the processed and behavioural feature engineering for a
    single transaction by reusing the shared pipeline modules
    (`src.data_processing.process_data.engineer_features` and
    `src.feature_engineering.features.engineer_features`), so the
    application cannot drift from the training-time definitions. The
    dataset-level thresholds used by the behavioural features
    (`is_large_transaction`, `is_late_step`) come from the persisted
    `inference_thresholds` rather than being recomputed from the
    single input row
  - `prepare_transaction` → exact 33-feature matrix; `predict` →
    `{"prediction": 0|1, "fraud_probability": float}`

- **`app/utils.py`** — investigation-priority helpers:
  `get_investigation_priority` (Low < 0.25 ≤ Moderate < 0.50 ≤ High
  < 0.75 ≤ Critical) and `get_priority_description`.

- **`app/streamlit_app.py`** — Streamlit UI: transaction inputs
  (type, amount, step, balances), cached model loading, result metrics
  (fraud probability, prediction, investigation priority) and
  interpretation text.

- **`tests/app/`** — `test_model_service.py`, `test_streamlit_app.py`
  and `test_utils.py` exercising the service class, the UI module, and
  the priority helpers.

- **Final-model training** — `src/machine_learning/train_final_model.py`:
  trains the final Random Forest on the full processed dataset and saves
  the model plus a feature schema that records the 33 features and the
  inference thresholds (`large_transaction_amount` = 0.99 quantile of
  amount, `late_step` = 0.90 quantile of step) to `models/`.

## How to Reproduce

```bash
# 1. Train and export the final model (requires the processed dataset)
python -m src.machine_learning.train_final_model

# 2. Run the UI
python -m streamlit run app/streamlit_app.py
```

## Related Documentation

- `docs/application/application-overview.md` — application architecture
- `docs/phase-9/explainability-and-fraud-investigation.md` — the priority
  semantics reused by the app
- `docs/phase-13/deployment.md` — how the app is intended to be deployed
- `docs/phase-0/project-requirements.md` — application requirements (§11,
  §12) and non-goals