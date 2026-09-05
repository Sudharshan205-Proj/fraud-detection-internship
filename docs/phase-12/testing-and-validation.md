# Phase 12 — Testing and Validation

## 1. Objective

Phase 12 validates the Fraud Detection System as an integrated project.

The objective is to verify that the data-processing, feature-engineering, machine-learning, inference, application, and visualization components operate consistently and that important project assumptions are protected by automated tests.

The testing strategy is appropriate for an internship-level educational system and focuses on correctness, regression prevention, reproducibility, data integrity, model-input consistency, and application behavior.

---

## 2. Testing Strategy

Testing is divided into the following areas:

1. Data validation
2. Feature-engineering validation
3. Model validation
4. Application validation
5. Reproducibility validation
6. Leakage prevention
7. Regression testing
8. Manual application validation
9. Visualization validation

The project uses `pytest` for automated Python testing.

---

## 3. Data Validation

Data validation tests verify important assumptions about transaction data.

The validation checks include:

- Required columns
- Missing values
- Duplicate rows
- Numeric data types
- Categorical transaction type
- Binary fraud target
- Binary flagged-fraud indicator
- Non-negative transaction amounts
- Non-negative account balances

The automated tests use small synthetic PaySim-style data so that validation does not require loading the full dataset.

---

## 4. Feature Validation

The feature-engineering validation checks that:

- Feature engineering preserves row count.
- Required engineered features are produced.
- The model feature set contains exactly 33 features.
- The fraud target is excluded.
- Transaction type is excluded from the final model feature set.
- `isFlaggedFraud` is excluded by default from the final model feature set.

The final model therefore receives a controlled feature schema rather than an uncontrolled set of input columns.

---

## 5. Model Validation

The final model is validated for:

- Successful model loading
- Correct model type
- Correct feature count
- Unique feature names
- Absence of the fraud target from model features
- Absence of raw transaction type from model features
- Presence of persisted inference thresholds
- Numeric inference thresholds
- Consistency between the model service and persisted feature schema

The expected final model feature count is:

**33 features**

The model artifacts are:

```text
models/random_forest_model.joblib
models/model_features.json
```

---

## 6. Application Validation

The Phase 10 application is validated for:

- All five transaction types produce a valid prediction
- Predictions are binary integers (0 or 1)
- Fraud probability is a float between 0 and 1
- Required result fields (`prediction`, `fraud_probability`) exist
- Investigation-priority mapping covers Low / Moderate / High / Critical
- Priority descriptions exist for every level
- Out-of-range probabilities are rejected
- Missing transaction fields are rejected with a clear error
- The Streamlit module imports successfully

---

## 7. Reproducibility Validation

Reproducibility is validated by:

- Stratified splits with a fixed random state produce identical
  train/test partitions
- Train and test indices never overlap
- The fraud target is never used as a model feature
- The persisted feature schema records the project's fixed random seed
- The final model exposes exactly 33 features

---

## 8. Deployment Validation

Deployment artifacts are validated by:

- The model artifact exists and is non-empty
- The model can be loaded with `joblib`
- The model expects exactly 33 features
- The feature schema exists and is valid JSON
- The schema contains the 33-feature list and both inference
  thresholds (`large_transaction_amount`, `late_step`)
- The Streamlit app, model service, and utility modules exist
- `requirements.txt` declares streamlit, pandas, numpy, joblib, and
  scikit-learn

---

## 9. Running the Validation Suite

```bash
python -m pytest tests/validation -q
```

The full project suite (including the Phase 12 validation area) runs
with:

```bash
python -m pytest
```

All tests are dataset-free: they use small synthetic PaySim-style
frames or inspect committed artifacts, so the suite runs in a fresh
checkout without the 6.3M-row dataset.

---

## 10. Status

Phase 12 testing and validation: **Complete**