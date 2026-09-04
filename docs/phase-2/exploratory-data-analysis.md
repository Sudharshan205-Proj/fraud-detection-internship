# Phase 2 — Exploratory Data Analysis

## Objective

Understand the structure, variables, data types, completeness,
transaction categories, and fraud distribution of the PaySim dataset
before any cleaning, transformation, or modelling.

This phase belongs to the **Prepare** stage of the project methodology
(Ask → Prepare → Process → Analyze → Share → Act).

## Status

**Complete** — matches the project-status table in the README.

## What Was Produced

- **Inspection notebook** — `notebooks/01_paysim_initial_inspection.ipynb`.

  The notebook works in two passes:

  1. A **10,000-row sample** establishes structure quickly without loading
     the full file: columns, dtypes, missing values, duplicates, transaction
     types, fraud counts, flagged-fraud crosstab, amount and step ranges,
     identifier cardinality.
  2. A **full-dataset pass** establishes definitive statistics: 6,362,620
     rows, 11 variables, no missing values, no exact duplicate rows,
     fraud rate (8,213 fraudulent transactions, ≈0.129%), fraud counts and
     percentages by transaction type, amount statistics overall and by
     fraud status, `isFlaggedFraud` crosstabs, step range and distribution,
     and account-identifier reuse.

- **No modification principle** — the notebook explicitly performs
  inspection only; records and variables are not removed during this
  phase. Problems found here are documented and addressed during
  processing (Phase 1) and later phases.

## Key Findings

- Severe class imbalance: ≈0.129% of transactions are fraudulent, which
  motivates the fraud-focused evaluation metrics and SMOTE treatment in
  later phases.
- `nameOrig` / `nameDest` are high-cardinality identifiers — not suitable
  as direct model features (removed in Phase 1, excluded in Phase 3).
- The existing `isFlaggedFraud` flag is extremely sparse and requires
  assessment before any model may use it.
- Fraud concentrates in specific transaction types (TRANSFER/CASH_OUT),
  informing the engineered features created in Phases 1 and 3.

## How to Reproduce

```bash
# Requires data/raw/PS_20174392719_1491204439457_log.csv
jupyter notebook notebooks/01_paysim_initial_inspection.ipynb
```

Notebook outputs are intentionally stripped from the committed file; the
recorded findings live in the dataset documentation below.

## Related Documentation

- `docs/data/dataset-documentation.md` — dataset source, structure, and metadata
- `docs/data/data-dictionary.md` — variable meanings and types
- `docs/data/data-quality-report.md` — quality assessment derived from inspection
- `docs/data/processed-dataset.md` — the processed layout that followed
- `docs/phase-1/data-processing.md` — the next phase