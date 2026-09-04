# Project Architecture

## 1. Overview

The Fraud Detection System is organised as a small Python library
(`src/`) plus thin runnable entry points (`scripts/`), a pytest suite
(`tests/`), documentation (`docs/`), and generated artifacts
(`results/`).

The guiding rules are:

* **`src/` holds importable, testable code.** No stage logic lives
  directly in an entry-point script.
* **`scripts/` holds thin runners.** Scripts parse arguments (e.g.
  `--max-rows`), call `src/` functions, and write artifacts.
* **Imports always go through the `src` package** (`from
  src.machine_learning.prepare import ...`). Installed via
  `pip install -e .`, this works from any working directory without
  `PYTHONPATH`.
* **Documentation never depends on regenerated artifacts.** Human
  explanations live in `docs/`; regenerable CSV/PNG outputs live in
  `results/` (see section 5).

## 2. Repository layout

```text
src/
├── __init__.py
├── data_processing/process_data.py    # canonical raw -> 24-col pipeline
├── feature_engineering/features.py    # 24 -> 36 columns + feature list
├── machine_learning/
│   ├── prepare.py                     # target split, encoding, split, SMOTE
│   ├── models.py                      # model factories (RF / LR config)
│   ├── evaluation.py                  # supervised model metrics
│   ├── metrics.py                     # shared metric helpers
│   ├── optimization.py                # threshold analysis
│   ├── validation.py                  # leakage / correlation analysis
│   ├── explainability.py              # feature importance + plots
│   ├── model_comparison.py            # comparison table + charts
│   └── (no entry points — those live in scripts/)
├── anomaly_detection/
│   ├── isolation_forest.py            # Isolation Forest helpers
│   ├── autoencoder.py                 # Keras autoencoder helpers
│   └── pipeline.py                    # orchestrates both detectors
├── analysis/fraud_investigation.py    # transaction-level investigation
└── sql_analysis/database.py           # SQLite database + query helpers

scripts/                               # all entry points
├── train_baseline.py                  # Phase 5/6 baseline models
├── generate_random_forest_predictions.py
├── model_optimization.py              # Phase 6 threshold analysis
├── leakage_analysis.py                # Phase 6 leakage analysis
├── model_explainability.py            # Phase 9 feature importance
├── run_model_comparison.py            # Phase 8 comparison (4 models)
├── check_database.py                  # SQLite inspection

tests/
├── helpers.py                         # synthetic PaySim frame builders
├── data/  sql/  anomaly_detection/    # area-scoped tests
└── test_*.py                          # feature tests (root level)

notebooks/   sql/                      # Jupyter inspection, SQL queries
data/        raw + processed CSV       # gitignored
results/     generated CSV/PNG/MD      # machine-learning artifacts
docs/        human-written reports     # phase + topic documentation
app/ r/ tableau/                       # placeholders (later phases)
```

## 3. Package responsibilities

| Package / module | Responsibility |
|---|---|
| `src.data_processing` | Single source of truth for the processed dataset: validation, the 15 engineered features, dtype-aware loading, and the processing report. `load_processed_dataset()` is the shared loader used by every downstream script. |
| `src.feature_engineering` | Adds the 12 behavioural features (24 → 36 columns) and returns the 33-feature model list. |
| `src.machine_learning` | Everything between processed data and evaluation: preparation, model factories, metric helpers, threshold optimization, leakage/correlation validation, explainability, comparison. |
| `src.anomaly_detection` | Isolation Forest + autoencoder implementations and the pipeline that trains and evaluates them on a single feature matrix. |
| `src.analysis` | Fraud-investigation support used to produce the transaction-level report. |
| `src.sql_analysis` | SQLite database creation (chunked CSV import) and query helpers. |
| `scripts/` | Thin runners that wire the above together and write artifacts. |

## 4. Data flow

```text
data/raw/PS_..._log.csv               11 columns
        │  src.data_processing.process_data
        ▼
data/processed/paysim_processed.csv   24 columns (9 original + 15 engineered)
        │
        ├── src.sql_analysis.database ──► data/paysim.db  (chunked import)
        │                                    └── run with sql/ queries
        ├── src.machine_learning.prepare ──► feature matrices (one-hot type)
        │                                    └── scripts/train_baseline.py
        ├── scripts/generate_random_forest_predictions.py ──► predictions CSV
        │                                    └── scripts/model_optimization.py
        ├── src.feature_engineering ──► 36-column engineered dataset
        ├── scripts/leakage_analysis.py ──► correlation CSV
        ├── scripts/model_explainability.py ──► importance CSV/PNG
        ├── src.analysis.fraud_investigation ──► investigation CSV
        └── src.anomaly_detection.pipeline ──► Isolation Forest + autoencoder
```

## 5. Artifact conventions

* **Generated, re-runnable outputs** (predictions, threshold tables,
  leakage correlations, comparison charts/reports) go under
  `results/`:
  * `results/machine-learning/random-forest-predictions.csv`
  * `results/machine-learning/threshold-analysis.csv`
  * `results/machine-learning/leakage-analysis-results.csv`
  * `results/model_comparison/` (comparison CSV, PNG, selection MD)
* **Case-study evidence embedded in documentation** stays with the
  docs that reference it:
  * `docs/machine-learning/explainability/` — feature-importance
    CSV/PNG and the fraud-investigation report, referenced by
    `model-explainability.md`.
* `data/*.csv`, `*.png` regenerable artifacts are gitignored except
  where they were deliberately committed earlier; regenerating them is
  always possible with the scripts in section 6 of the README.

## 6. Memory strategy

The full PaySim file has 6.36M rows, so the code is written to keep
peak memory bounded:

* **Dtype-aware loading**: money columns stay `float64`; `step` and
  binary indicators are small integers (`int16`/`int8`); engineered
  ratios and `log_amount` are `float32`.
* **No defensive copies**: feature engineering adds columns in place on
  the freshly loaded frame.
* **Shared loaders**: all scripts use
  `load_processed_dataset(path, max_rows=None)` instead of re-reading
  with ad hoc settings.
* **Sample mode**: every heavy entry point accepts `--max-rows N` for
  quick runs on modest hardware (default: full dataset).
* **Chunked SQLite import**: the CSV → SQLite copy streams in 100k-row
  chunks (this is the one place chunking is genuinely implemented).

## 7. Packaging

`pyproject.toml` provides:

* setuptools build configuration (`include = ["src*"]`);
* the pytest configuration (`pythonpath = ["."]`, `testpaths =
  ["tests"]`) that used to live in `pytest.ini`;
* project metadata.

Runtime dependency **pins** intentionally live only in
`requirements.txt` so there is a single source of truth.

After `pip install -e .`:

```bash
python scripts/leakage_analysis.py --help     # works from any directory
python -m src.anomaly_detection.pipeline      # module invocation also works
```

## 8. Terminology quick reference

See the README table. In short: raw 11 → processed **24 columns**
(**15 engineered**) → feature-engineered **36 columns** → **33 model
features**. Numbers are asserted by the tests
(`tests/data/test_process_data.py`,
`tests/test_end_to_end_pipeline.py`).
