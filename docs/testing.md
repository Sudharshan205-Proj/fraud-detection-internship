# Testing

## 1. Running the suite

```bash
python -m pytest                      # everything
python -m pytest tests/data -q        # data-processing tests only
python -m pytest tests/sql -q         # SQLite query tests
python -m pytest tests/anomaly_detection -q
python -m pytest tests/test_end_to_end_pipeline.py -q
python -m pytest tests/test_threshold_analysis.py -q
```

The pytest configuration (test paths + `pythonpath`) lives in
`pyproject.toml`, not a separate `pytest.ini`.

**The suite never needs the real PaySim dataset.** All end-to-end tests
generate small, deterministic, PaySim-style frames and write only under
pytest's `tmp_path`; they never touch `data/` or `docs/` output paths.

## 2. Test layout

```text
tests/
├── helpers.py                        # shared synthetic-data builders
├── data/
│   └── test_process_data.py          # canonical processing module
├── sql/
│   └── test_sql_analysis.py          # in-memory SQLite query tests
├── anomaly_detection/
│   └── test_anomaly_detection.py     # unit tests + anomaly e2e runs
├── test_baseline_models.py           # model factories, evaluation
├── test_feature_engineering.py       # 36-column feature stage
├── test_machine_learning.py          # prepare/split/SMOTE/threshold units
├── test_explainability.py            # importance/permutation/plots
├── test_model_comparison.py          # comparison helpers
├── test_fraud_investigation.py       # investigation report helpers
├── test_end_to_end_pipeline.py       # processing -> model-prep e2e
└── test_threshold_analysis.py        # predictions -> threshold e2e
```

## 3. What the dataset-free e2e tests cover

* `test_end_to_end_pipeline.py` — writes a synthetic raw CSV, runs the
  canonical processing pipeline (load → validate → engineer → save),
  reloads the file, and asserts the **24-column layout** (exact column
  order, dtypes, identifier removal, no NaN/inf). It then runs the
  model-preparation flow (target split, one-hot `type`, stratified
  split, Random Forest training, evaluation metrics).
* `test_threshold_analysis.py` — generates Random Forest predictions
  from a synthetic processed frame, writes the predictions CSV, feeds
  it through `scripts/model_optimization.analyze_predictions`, and
  checks the full threshold grid, metric ranges, and best-threshold
  selection.
* `tests/anomaly_detection/test_anomaly_detection.py` — runs the
  Isolation Forest and autoencoder pipeline end to end on a small
  synthetic processed frame and checks the metric contract returned by
  both detectors.

These tests pin the documented pipeline story: **24 columns = 9
original + 15 engineered**, **36-column** feature-engineered dataset,
**33 model features**, and single-float64-matrix anomaly preparation.

## 4. How the synthetic data helpers work

`tests/helpers.py` provides:

* `make_synthetic_raw_rows(n_rows)` — deterministic PaySim-style rows:
  every 10th row is fraudulent (alternating TRANSFER/CASH_OUT with zero
  origin balances); legitimate rows keep exact balance consistency.
* `make_processed_frame(n_rows)` — runs the real
  `process_dataset()` over those rows, yielding a genuine 24-column
  processed frame.

Use these helpers when a test needs realistic data without the 6.3M-row
CSV.

## 5. Adding a test

1. Place module tests next to their subject (`tests/data/`,
   `tests/sql/`, `tests/anomaly_detection/`) or as
   `tests/test_<feature>.py` for cross-module features.
2. Build input data with `tests/helpers.py` or a small fixture; write
   any CSV/artifact under `tmp_path`.
3. Never point tests at `data/` or `docs/` output paths — the suite
   must be runnable in a fresh checkout.
4. Keep assertions on behaviour (layout, metrics, contract) rather than
   re-stating fixture content.

## 6. What is intentionally not covered

Training/evaluation against the full 6.36M-row dataset is not part of
the automated suite (hours of runtime, multi-GB RAM). To validate a
full run locally:

```bash
python -m src.data_processing.process_data               # needs data/raw file
python scripts/train_baseline.py --max-rows 500000       # quick sanity first
python scripts/train_baseline.py                         # full data
```
