# Runbook — Fraud Detection System (Phases 1–13)

Step-by-step guide to every command to run, in dependency order, with the
expected output for each. Covers the `R/`, `scripts/`, `sql/`, `src/`,
and `tests/` folders. All commands run from the **project root**.

## 0. One-time setup (do this first)

```bash
# Create + activate a virtual environment
python -m venv .venv
# Windows:  .venv\Scripts\activate      macOS/Linux: source .venv/bin/activate

# Install pinned dependencies and register the src package
pip install -r requirements.txt
pip install -e .
```

- Place the PaySim file at `data/raw/PS_20174392719_1491204439457_log.csv`.
- Verify the environment:

```bash
python -c "import pandas, sklearn, joblib, streamlit, tensorflow; print('deps OK')"
# Expected: deps OK
```

**Ordering rules** (the pipeline builds on itself):

| Command needs... | Produced by... |
|---|---|
| `data/processed/paysim_processed.csv` | Phase 1 processing |
| `data/paysim.db` | Phase 4 database build |
| `results/machine-learning/random-forest-predictions.csv` | Phase 6 predictions script |
| `results/model_comparison/model_comparison.csv` | Phase 8 comparison script |
| `models/random_forest_model.joblib` + `models/model_features.json` | Phase 10 final-model training |
| `data/visualization/*.csv` | Phase 11 visualization-data script |

> **Heavy runs:** several full-dataset commands need ~8–16 GB RAM and can
> take minutes to hours. Most accept `--max-rows N` for a fast smoke test.
> Run the smoke test first, then the full command.

---

## Phase 1 — Data Processing & Cleaning (`src/`, `tests/`)

### 1.1 Process the raw dataset

```bash
python -m src.data_processing.process_data
```

**Expected output:**

```text
Loading raw PaySim dataset...
Rows loaded: 6,362,620
Columns loaded: 11

Validation results:
missing_values: 0
duplicate_rows: 0
invalid_transaction_types: 0
invalid_isFraud_values: 0
invalid_isFlaggedFraud_values: 0
negative_financial_values: 0
empty_origin_ids: 0
empty_destination_ids: 0

Processing complete.
Processed dataset: data\processed\paysim_processed.csv
Processing report: docs\data\processing-report.md
Processed rows: 6,362,620
Processed columns: 24
```

**Artifacts:** `data/processed/paysim_processed.csv` (24 columns = 9
retained originals + 15 engineered) and the regenerated
`docs/data/processing-report.md`.

### 1.2 Run the Phase 1 tests

```bash
python -m pytest tests/data -q
# Expected: 25 passed in ~1.5s
```

```bash
python -m pytest tests/test_end_to_end_pipeline.py -q
# Expected: 2 passed in ~2.3s   (dataset-free raw→processed→model-prep e2e)
```

---

## Phase 2 — Exploratory Data Analysis (`notebooks/`)

Inspection only — no script or test to run. Execute the notebook cell by
cell:

```bash
jupyter notebook notebooks/01_paysim_initial_inspection.ipynb
```

**Expected findings (printed in the notebook):**

- 6,362,620 rows · 11 columns · **no missing values** · **no duplicate rows**
- Fraud rate: 8,213 fraudulent transactions ≈ **0.129%**
- 5 transaction types: CASH_IN, CASH_OUT, DEBIT, PAYMENT, TRANSFER
- Fraud concentrates in TRANSFER / CASH_OUT only
- `isFlaggedFraud` is extremely sparse (16 flagged rows, all fraud)

---

## Phase 3 — Feature Engineering (`src/`, `tests/`)

No standalone CLI — `src/feature_engineering/features.py` is consumed by
the Phase 6+ entry points (24 → **36 columns**, **33 model features**).
Verify it with the tests:

```bash
python -m pytest tests/test_feature_engineering.py -q
# Expected: 11 passed in ~0.7s
```

---

## Phase 4 — SQL Analysis (`src/`, `scripts/`, `sql/`, `tests/`)

### 4.1 Build the SQLite database from the processed CSV

```bash
python -m src.sql_analysis.database
```

**Expected output:**

```text
SQLite database successfully created: <project>\data\paysim.db
```

### 4.2 Inspect the database

```bash
python scripts/check_database.py
```

**Expected output (verified):**

```text
Tables:
- transactions

Transaction rows: 6,362,620
Fraudulent rows: 8,213
```

### 4.3 Run the SQL analysis scripts (against `data/paysim.db`)

```bash
sqlite3 -header -column data/paysim.db < sql/02_basic_queries.sql
sqlite3 -header -column data/paysim.db < sql/03_fraud_analysis.sql
sqlite3 -header -column data/paysim.db < sql/04_aggregation.sql
sqlite3 -header -column data/paysim.db < sql/05_joins.sql
sqlite3 -header -column data/paysim.db < sql/06_subqueries.sql
sqlite3 -header -column data/paysim.db < sql/07_temp_tables.sql
sqlite3 -header -column data/paysim.db < sql/08_validation.sql
```

**Expected outputs (key rows):**

- `02_basic_queries.sql`: total 6,362,620 · fraud 8,213 · legitimate
  6,354,407 · 5 types · top-20 amounts (largest 92,445,516.64) ·
  **743** unique steps.
- `03_fraud_analysis.sql`: overall fraud rate **0.129063%**; fraud by
  type — CASH_OUT 4,116, TRANSFER 4,097, others 0; amount stats by
  fraud status; fraud by step; top-20 high-value frauds; flag check —
  `isFlaggedFraud=1` → 16 rows, all 16 actually fraudulent.
- `04_aggregation.sql`: volume by type — CASH_OUT 2,237,500 · PAYMENT
  2,151,495 · CASH_IN 1,399,284 · TRANSFER 532,909 · DEBIT 41,432;
  fraud volume by type; types with > 100,000 transactions; per-step
  activity (743 rows).
- `05_joins.sql`: 100 joined rows (transactions + type-level summary).
- `06_subqueries.sql`: 100 largest above-average transactions; types
  above overall fraud rate (TRANSFER, CASH_OUT).
- `07_temp_tables.sql`: per-type fraud summary ordered by fraud count.
- `08_validation.sql`: row_count 6,362,620; `isFraud` ∈ {0,1}; 5 types;
  negative amounts **0**; missing types **0**; missing labels **0**;
  inconsistent balance rows **> 0** (only fraud-type rows violate balance
  consistency); flagged 16 / flagged fraud 16.

> `01_database_setup.sql` only **defines** the schema — the actual data
> import happens in step 4.1 (`src.sql_analysis.database`). Running it
> through `sqlite3` drops and recreates an **empty** `transactions`
> table, so only run it if you re-run step 4.1 afterwards.

### 4.4 Run the SQL tests

```bash
python -m pytest tests/sql -q
# Expected: 5 passed in ~0.7s
```

---

## Phase 5 — Machine Learning Preparation (`src/`, `tests/`)

No standalone CLI — `src/machine_learning/prepare.py` (split, one-hot
encoding, scaling, SMOTE) is exercised by the Phase 6 scripts. Verify
with the tests:

```bash
python -m pytest tests/test_machine_learning.py -q
# Expected: 18 passed in ~2.1s
```

---

## Phase 6 — Supervised Machine Learning (`scripts/`, `tests/`)

Run in this order — step 6.3 consumes step 6.2's output.

### 6.1 Train baseline models

Quick smoke test first, then the full run:

```bash
python scripts/train_baseline.py --max-rows 500000
python scripts/train_baseline.py
```

**Expected output shape:**

```text
Sample mode active: using at most 500,000 rows.      # only with --max-rows

Training Logistic Regression...
Logistic Regression Results
accuracy: 0.967201
precision: 0.034137
recall: 0.894096
f1_score: 0.065762
roc_auc: 0.984229

Training Random Forest...
Random Forest Results
accuracy: 0.999995
precision: 0.998781
recall: 0.997565
f1_score: 0.998173
roc_auc: 0.999087
```

(The metric values above are the verified **full-dataset** results;
`--max-rows` sample runs print different, lower numbers — that is
expected.)

### 6.2 Generate held-out predictions

```bash
python scripts/generate_random_forest_predictions.py [--max-rows N]
```

**Expected output:**

```text
Loading processed dataset...
Training Random Forest...
Prediction generation complete.
Rows: 1,272,524                    # 20% of 6,362,620 (fewer with --max-rows)
Fraudulent test observations: 1,643
Saved to: results\machine-learning\random-forest-predictions.csv
```

**Artifact:** `results/machine-learning/random-forest-predictions.csv`
(columns `actual`, `probability`).

### 6.3 Threshold optimization (needs 6.2's CSV)

```bash
python scripts/model_optimization.py
```

**Expected output (verified):**

```text
Threshold analysis complete.

Best threshold based on F1-score:
threshold    0.600000
precision    1.000000
recall       0.997565
f1_score     0.998781
roc_auc      0.999087
accuracy     0.999997

Results saved to: results\machine-learning\threshold-analysis.csv
```

### 6.4 Leakage analysis

```bash
python scripts/leakage_analysis.py [--max-rows N]
```

**Expected output shape:**

```text
Loading processed dataset...
Rows: 6,362,620
Columns: 24

Identifier columns:
- None

Features requiring leakage assessment:
- isFlaggedFraud

Target correlations:
<correlation table, isFlaggedFraud ~0.999 and log_amount highly correlated>

Results saved to: results\machine-learning\leakage-analysis-results.csv
```

### 6.5 Phase 6 tests

```bash
python -m pytest tests/test_baseline_models.py -q
# Expected: 6 passed in ~1.9s
python -m pytest tests/test_threshold_analysis.py -q
# Expected: 3 passed in ~2.2s
```

---

## Phase 7 — Anomaly Detection (`src/`, `tests/`)

### 7.1 Run the anomaly pipeline

Smoke test first, then the full run (the full run trains a Keras
autoencoder over ~5M rows — heavy):

```bash
python -m src.anomaly_detection.pipeline --max-rows 100000
python -m src.anomaly_detection.pipeline
```

**Expected output shape:**

```text
Loading processed PaySim dataset...
Dataset shape: (6362620, 24)
Feature matrix shape: (6362620, 27)

Running Isolation Forest...
Isolation Forest Results
precision: 0.035260
recall: 0.270237
f1_score: 0.062381
roc_auc: 0.893615

Running Autoencoder...
<keras per-epoch progress bars>

Autoencoder Results
precision: 0.085778
recall: 0.722459
f1_score: 0.153349
roc_auc: 0.943997

Autoencoder threshold: <value>
```

(The metrics above are the verified full-dataset results. The
autoencoder is a neural network, so its numbers vary slightly between
runs; Isolation Forest is deterministic given `random_state=42`.)

### 7.2 Anomaly tests

```bash
python -m pytest tests/anomaly_detection -q
# Expected: 8 passed in ~17s   (unit tests + dataset-free Isolation Forest/autoencoder e2e)
```

---

## Phase 8 — Model Comparison & Selection (`scripts/`, `tests/`)

### 8.1 Generate the comparison report

```bash
python scripts/run_model_comparison.py
```

**Expected output (verified):**

```text
Phase 8 Model Comparison
============================================================
              model  accuracy  precision   recall  f1_score  roc_auc
      Random Forest  0.999995   0.998781 0.997565  0.998173 0.999087
        Autoencoder       NaN   0.085778 0.722459  0.153349 0.943997
Logistic Regression  0.967201   0.034137 0.894096  0.065762 0.984229
   Isolation Forest       NaN   0.035260 0.270237  0.062381 0.893615
============================================================

Best model by F1-score: Random Forest
Best model by Recall: Random Forest
Best model by Precision: Random Forest

Artifacts created:
- results\model_comparison\model_comparison.csv
- results\model_comparison\model_comparison.png
- results\model_comparison\model_selection.md
```

### 8.2 Comparison tests

```bash
python -m pytest tests/test_model_comparison.py -q
# Expected: 8 passed in ~1.5s
```

---

## Phase 9 — Explainability & Fraud Investigation (`scripts/`, `src/`, `tests/`)

### 9.1 Feature importance

```bash
python scripts/model_explainability.py [--max-rows N]
```

**Expected output shape:**1

```text
Loading processed dataset...
Rows: 6,362,620
Columns: 24
Prepared features: 27

Training Random Forest for explainability...
Model trained successfully.

Top 15 Features
============================================================
<feature  importance  importance_percent>
...

Feature importance saved:
docs\machine-learning\explainability\random-forest-feature-importance.csv

Feature importance chart saved:
docs\machine-learning\explainability\random-forest-feature-importance.png
```

### 9.2 Transaction-level investigation report

```bash
python -m src.analysis.fraud_investigation [--max-rows N]
```

**Expected output shape:**

```text
Loading processed dataset...
Rows: 6,362,620
Columns: 24

Preparing model features...
Feature matrix: (6362620, 27)

Training Random Forest...
Model trained successfully.

Creating investigation report...

Investigation report saved:
docs\machine-learning\explainability\fraud-investigation-report.csv

Top 10 highest-risk transactions:
<10 rows with fraud_probability, predicted_fraud, investigation_priority>
```

**Artifact:** `docs/machine-learning/explainability/fraud-investigation-report.csv`
— every transaction with `fraud_probability` and priority
(Low < 0.25 ≤ Moderate < 0.50 ≤ High < 0.75 ≤ Critical), sorted for triage.

### 9.3 Phase 9 tests

```bash
python -m pytest tests/test_explainability.py -q
# Expected: 7 passed in ~6.4s
python -m pytest tests/test_fraud_investigation.py -q
# Expected: 5 passed in ~3.3s
```

---

## Phase 10 — Application Development (`src/`, `app/`, `tests/`)

### 10.1 Train and export the final model (needs the processed CSV)

```bash
python -m src.machine_learning.train_final_model
```

**Expected output shape:**

```text
Loading processed dataset...
Original shape: (6362620, 24)
Engineered shape: (6362620, 36)
Model feature count: 33
Fraud transactions: 8213
Legitimate transactions: 6354407

Splitting data...
Training rows: 5,090,096
Testing rows: 1,272,524

Creating Random Forest...
Training Random Forest...
Training complete.

Saving model to: models\random_forest_model.joblib
Model saved successfully.
Feature schema saved to: models\model_features.json

Final model summary
-------------------
Model: Random Forest
Features: 33
Model file: models\random_forest_model.joblib
Schema file: models\model_features.json
```

**Artifacts:** `models/random_forest_model.joblib` +
`models/model_features.json` (33 features + inference thresholds
`large_transaction_amount`, `late_step`).

### 10.2 Run the Streamlit UI

```bash
python -m streamlit run app/streamlit_app.py
```

**Expected output:** the dev server starts at
`http://localhost:8501` ("You can now view your Streamlit app..."). Open
it in a browser, enter a transaction, and you get fraud probability,
prediction, and investigation priority. Press `Ctrl+C` to stop it.

### 10.3 Application tests

```bash
python -m pytest tests/app -q
# Expected: 24 passed in ~3.4s
#  - test_model_service.py: inference service against the 33-feature schema
#  - test_utils.py: priority helpers
#  - test_streamlit_app.py: UI module imports
```

---

## Phase 11 — Visualization & Tableau (`scripts/`, `R/`, `data/`)

Run in this order — each step consumes the previous one's output.

### 11.1 Generate compact visualization datasets

```bash
python scripts/generate_visualization_data.py
```

**Expected output shape (verified):**

```text
==============================================================
PHASE 11 - VISUALIZATION DATA GENERATION
==============================================================
Input: data/processed/paysim_processed.csv

Processed chunk 1: 250,000 transactions
... (chunk progress, ~26 chunks)
Processed chunk 26: 6,362,620 transactions

Creating visualization datasets...
Copied model performance from: results\model_comparison\model_comparison.csv

==============================================================
VISUALIZATION DATA GENERATION COMPLETE
==============================================================
Total transactions: 6,362,620
Fraud transactions: 8,213
Fraud rate: 0.1291%

Generated:
  data/visualization/fraud_dashboard_data.csv
  data/visualization/fraud_summary.csv
  data/visualization/fraud_by_type.csv
  data/visualization/fraud_by_step.csv
  data/visualization/fraud_by_amount.csv
  data/visualization/model_performance.csv
```

> Needs `results/model_comparison/model_comparison.csv` (Phase 8) — else
> it prints a WARNING and skips `model_performance.csv`.

### 11.2 Generate Python charts

```bash
python scripts/create_visualizations.py
```

**Expected output:**

```text
======================================================================
PHASE 11 PYTHON VISUALIZATIONS COMPLETE
======================================================================

Generated figures:
  reports/figures/fraud_distribution.png
  reports/figures/fraud_by_type.png
  reports/figures/fraud_by_step.png
  reports/figures/fraud_by_amount.png
  reports/figures/model_performance.png
```

### 11.3 R analysis

```bash
Rscript r/fraud_analysis.R
```

**Expected output (verified):**

```text
PHASE 11 - R FRAUD ANALYSIS
============================

Overall summary:
  Total Transactions          6.36e+6
  Fraud Transactions          8.21e+3
  Legitimate Transactions     6.35e+6
  Fraud Rate (%)              1.29e-1
  Total Transaction Amount    1.14e+12
  Average Transaction Amount  1.80e+5
  Minimum Transaction Amount  0
  Maximum Transaction Amount  9.24e+7

Fraud by transaction type:
  TRANSFER  532,909 total / 4,097 fraud  -> 0.769%
  CASH_OUT  2,237,500 total / 4,116 fraud -> 0.184%
  CASH_IN, DEBIT, PAYMENT -> 0 fraud

Transaction type with highest fraud rate: TRANSFER
Simulation-step analysis: 6,362,620 total / 8,213 fraud / 0.129 avg rate
Amount-range analysis: <fraud rate by amount bin, highest in 1,000,001+>
Best model by F1-score: Random Forest
Best model by ROC-AUC: Random Forest
R analysis complete.
```

(dplyr startup messages about masked objects are normal.)

### 11.4 R visualizations

```bash
Rscript r/fraud_visualization.R
```

**Expected output:** `R visualizations created successfully.` and 4 PNGs
written to `reports/figures/`: `r_fraud_by_type.png`,
`r_fraud_by_step.png`, `r_fraud_by_amount.png`, `r_model_performance.png`.

### 11.5 Knit the R Markdown report

```bash
Rscript -e "rmarkdown::render("r/fraud_analysis.Rmd")"
```

**Expected output:** `r/fraud_analysis.html` is produced (or knitted via
RStudio's "Knit" button).

### 11.6 Tableau dashboard (manual, no CLI)

Open `tableau/fraud_detection_dashboard.twbx` in Tableau Public. The
dashboard shows total transactions, fraud transactions, fraud rate,
fraud by type, fraud across steps, amount analysis, and model
performance, with filters (type / fraud status / step / amount range).

---

## Phase 12 — Testing & Validation (`tests/`)

### 12.1 Phase 12 validation suite

```bash
python -m pytest tests/validation -q
# Expected: 56 passed in ~4.2s
```

Covers data validation, feature-schema contract (33 features), final
model + schema checks, application behaviour, reproducibility/leakage,
and deployment artifacts.

### 12.2 Full project suite

```bash
python -m pytest
# Expected: 178 passed (verified: 178 passed in ~18.6s)
```

Breakdown by area:

| Test area | Count |
|---|---|
| `tests/data` | 25 passed |
| `tests/app` | 24 passed |
| `tests/machine-learning units (test_baseline_models + test_machine_learning)` | 6 + 18 passed |
| `tests/feature engineering + e2e (test_feature_engineering + test_end_to_end_pipeline)` | 11 + 2 passed |
| `tests/threshold (test_threshold_analysis)` | 3 passed |
| `tests/anomaly_detection` | 8 passed |
| `tests/sql` | 5 passed |
| `tests/model comparison + explainability + fraud investigation` | 8 + 7 + 5 passed |
| `tests/validation` | 56 passed |

> The suite never needs the 6.3M-row dataset. Warnings about scikit-learn
> versions (`InconsistentVersionWarning`) come from unpickling model
> artifacts and are harmless.

---

## Phase 13 — Deployment (`tests/`, `app/`)

### 13.1 Deployment validation tests

```bash
python -m pytest tests/validation/test_deployment_validation.py -q
# Expected: all passed (part of the 56)
```

Checks that the model artifact exists/loads with 33 features, the
feature schema is valid JSON with both inference thresholds, the app
files exist, and `requirements.txt` declares the required packages.

### 13.2 Local deployment

```bash
# 1. Install (if not already done)
pip install -r requirements.txt
pip install -e .

# 2. Train/export the final model (if not already done — Phase 10.1)
python -m src.machine_learning.train_final_model

# 3. Launch the app
streamlit run app/streamlit_app.py
```

**Expected output:** server on `http://localhost:8501` (headless mode;
usage stats disabled per `.streamlit/config.toml`). Enter transaction
details → fraud probability, prediction (0/1), investigation priority.

### 13.3 Streamlit Community Cloud (manual)

1. Push the repository to GitHub (model artifacts are committed, so a
   fresh clone has everything the app needs).
2. Create the app at https://share.streamlit.io connected to the repo.
3. Set the main file to `app/streamlit_app.py` — the cloud runs
   `pip install -r requirements.txt` automatically.

---

## Quick recap — run everything in order

```bash
# Phase 1
python -m src.data_processing.process_data
python -m pytest tests/data -q
# Phase 3 (Phase 2 is the inspection notebook)
python -m pytest tests/test_feature_engineering.py -q
# Phase 4
python -m src.sql_analysis.database
python scripts/check_database.py
# sqlite3 data/paysim.db < sql/02..08_*.sql
python -m pytest tests/sql -q
# Phase 5
python -m pytest tests/test_machine_learning.py -q
# Phase 6
python scripts/train_baseline.py --max-rows 500000
python scripts/generate_random_forest_predictions.py --max-rows 500000
python scripts/model_optimization.py
python scripts/leakage_analysis.py --max-rows 500000
python -m pytest tests/test_baseline_models.py tests/test_threshold_analysis.py -q
# Phase 7
python -m src.anomaly_detection.pipeline --max-rows 100000
python -m pytest tests/anomaly_detection -q
# Phase 8
python scripts/run_model_comparison.py
python -m pytest tests/test_model_comparison.py -q
# Phase 9
python scripts/model_explainability.py --max-rows 500000
python -m src.analysis.fraud_investigation --max-rows 500000
python -m pytest tests/test_explainability.py tests/test_fraud_investigation.py -q
# Phase 10
python -m src.machine_learning.train_final_model
streamlit run app/streamlit_app.py
python -m pytest tests/app -q
# Phase 11
python scripts/generate_visualization_data.py
python scripts/create_visualizations.py
Rscript r/fraud_analysis.R
Rscript r/fraud_visualization.R
Rscript -e 'rmarkdown::render("r/fraud_analysis.Rmd")'
# Phase 12
python -m pytest
# Phase 13
python -m pytest tests/validation/test_deployment_validation.py -q
streamlit run app/streamlit_app.py
```