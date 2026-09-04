# Phase 10 — Application Development

## Objective

Build a lightweight internship-level interface that scores individual
transactions with the selected Random Forest model and presents the
result as an analyst-facing fraud assessment with investigation
priority.

## Status

**In progress** — matches the project-status table in the README. The
model-training and service pieces exist and are tested; the Streamlit
UI is scaffolded but not yet runnable because a small amount of
wiring remains (see "Remaining Work").

## What Exists

The application code lives in the primary project folder (currently
untracked — it has not been committed yet):

- **`app/model_service.py`** — `FraudModelService`:

  - loads `models/random_forest_model.joblib` and
    `models/model_features.json`
  - validates that the model's expected feature count matches the
    persisted 33-feature schema
  - replicates the processed and behavioural feature engineering for a
    single transaction (balance changes/errors, zero-balance and type
    indicators, log/ratio features, threshold-based flags using the
    persisted `inference_thresholds`)
  - `prepare_transaction` → exact 33-feature matrix; `predict` →
    `{"prediction": 0|1, "fraud_probability": float}`

- **`app/utils.py`** — investigation-priority helpers:
  `get_investigation_priority` (Low < 0.25 ≤ Moderate < 0.50 ≤ High
  < 0.75 ≤ Critical) and `get_priority_description`.

- **`app/streamlit_app.py`** — Streamlit UI: transaction inputs
  (type, amount, step, balances), cached model loading, result metrics
  (fraud probability, prediction, investigation priority) and
  interpretation text. The UI currently imports module-level glue
  functions that are not yet defined (see below).

- **`tests/app/`** — `test_model_service.py` and `test_utils.py`
  exercising the service class and priority helpers.

- **Final-model training** — `src/machine_learning/train_final_model.py`:
  trains the final Random Forest on the full processed dataset and saves
  the model plus a feature schema that records the 33 features and the
  inference thresholds (`large_transaction_amount` = 0.99 quantile of
  amount, `late_step` = 0.90 quantile of step) to `models/`.

## Remaining Work

- `app/streamlit_app.py` imports `load_model` and `predict_transaction`
  from `app.model_service` and `get_prediction_message` from
  `app.utils`; those module-level glue functions are not defined yet
  (`model_service.py` currently exposes the `FraudModelService` class,
  and `utils.py` lacks `get_prediction_message`). Until they are added,
  `streamlit run` will fail on import.
- The `app/`, `models/`, and `tests/app/` files need to be committed.
- `train_final_model.py` requires the full processed dataset and several
  minutes of training before the model artifacts exist.

## How to Reproduce (once wiring is complete)

```bash
# 1. Train and export the final model (requires the processed dataset)
python -m src.machine_learning.train_final_model

# 2. Run the UI
python -m streamlit run app/streamlit_app.py
```

## Related Documentation

- `docs/phase-8/model-comparison.md` — why Random Forest was selected
- `docs/phase-9/explainability-and-fraud-investigation.md` — the priority
  semantics reused by the app
- `docs/phase-13/deployment.md` — how the app is intended to be deployed
- `docs/phase-0/project-requirements.md` — application requirements (§11,
  §12) and non-goals