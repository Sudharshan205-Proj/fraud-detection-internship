# Phase 1 — Data Processing and Cleaning

## Objective

Convert the raw PaySim CSV into a validated, cleaned, and feature-enriched
processed dataset that every later analysis stage consumes.

The phase follows the **Process** stage of the project methodology
(Ask → Prepare → Process → Analyze → Share → Act): validate, clean,
transform, and document the dataset before any modelling.

## Status

**Complete** — matches the project-status table in the README.

## What Was Produced

- **Canonical processing module** — `src/data_processing/process_data.py`:

  - `load_data` — dtype-aware raw loader with an optional `max_rows` cap
    (money stays `float64`; step/indicator columns use small integer
    dtypes to keep memory usage bounded on the 6.36M-row file).
  - `validate_schema` / `validate_values` / `validate_raw_data` — raise on
    missing columns, invalid values, and duplicate rows.
  - `engineer_features` — creates the 15 engineered features (balance
    changes and errors, zero-balance indicators, transaction-type
    indicators, log amount, balance ratios).
  - `remove_identifier_columns` — drops the high-cardinality `nameOrig`
    and `nameDest` identifiers.
  - `process_dataset` — orchestrates validation → engineering →
    identifier removal → CSV output.
  - `load_processed_dataset` — the shared dtype-aware loader used by all
    downstream phases.
  - `create_processing_report` — regenerates `docs/data/processing-report.md`
    so the committed report cannot drift from the code.

- **Processed dataset** — `data/processed/paysim_processed.csv`:

  - 6,362,620 rows · 24 columns = **9 original columns retained + 15
    engineered features**
  - Target `isFraud` retained; existing `isFlaggedFraud` retained for
    later investigation; account identifiers removed.
  - Class distribution preserved: 6,354,407 legitimate / 8,213 fraudulent.

- **Tests** — `tests/data/test_process_data.py` (schema, validation,
  engineered features, identifier removal, `max_rows`, round-trip) plus
  the dataset-free end-to-end suite in `tests/test_end_to_end_pipeline.py`.

## How to Reproduce

```bash
# Place the raw file at data/raw/PS_20174392719_1491204439457_log.csv,
# then run the canonical pipeline (regenerates the CSV and the report):
python -m src.data_processing.process_data
```

## Key Points

- The 24-column layout is the project's fixed terminology for the
  processed dataset — see `docs/data/processed-dataset.md`.
- No oversampling happens here; class imbalance is addressed during
  machine-learning preparation (Phase 5).
- The old `src/data/` package was consolidated into this module; it is
  the single source of truth for processing.

## Related Documentation

- `docs/data/data-processing.md` — narrative description of the pipeline
- `docs/data/processed-dataset.md` — 24-column layout specification
- `docs/data/data-dictionary.md` and `docs/data/dataset-documentation.md`
- `docs/data/data-quality-report.md` — pre-processing quality assessment
- `docs/data/processing-report.md` — generated pipeline report
- `docs/phase-2/exploratory-data-analysis.md` — the inspection that preceded
  processing