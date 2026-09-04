# Phase 12 — Testing and Validation

## Objective

Provide automated tests for the project's important components: data
loading, validation, feature preparation, prediction output, evaluation
calculations, and the application service layer.

## Status

**Implemented** — the suite currently passes **98 tests** and never
requires the 6.36M-row dataset. (The project-status table in the README
still lists this phase as Pending; this document reflects the actual
repository evidence.)

## What Was Produced

- **Test layout** — `tests/`:

  - `tests/helpers.py` — deterministic synthetic PaySim builders
    (`make_synthetic_raw_rows`, `make_processed_frame`) used by the
    dataset-free end-to-end suites
  - `tests/data/`, `tests/sql/`, `tests/anomaly_detection/` — area-scoped
    unit tests
  - `tests/test_*.py` — feature-level tests (processing, feature
    engineering, ML preparation/models, model comparison, explainability,
    fraud investigation, baselines, threshold analysis)
  - `tests/app/` — application-service tests (in the primary project
    folder; added with Phase 10)

- **Dataset-free end-to-end suites**:

  - `tests/test_end_to_end_pipeline.py` — raw CSV → processing →
    24-column layout → model preparation → training → evaluation
  - `tests/anomaly_detection/test_anomaly_detection.py` — Isolation
    Forest and autoencoder trained on a synthetic processed frame with
    metric-contract checks
  - `tests/test_threshold_analysis.py` — predictions CSV → threshold
    optimization workflow

- **Configuration** — `pyproject.toml` (`[tool.pytest.ini_options]`
  with `pythonpath = ["."]` and `testpaths = ["tests"]`), so tests run
  with no `PYTHONPATH` setup.

## How to Reproduce

```bash
python -m pytest                 # full suite
python -m pytest tests/data -q   # single area
```

## What Is Not Covered

- Full-dataset runs (they require the local PaySim file and are not part
  of the automated suite).
- The Streamlit UI layer itself (its wiring is still in progress —
  see `docs/phase-10/application-development.md`).

## Related Documentation

- `docs/testing.md` — test layout, run commands, and how to extend the suite
- `docs/phase-14/documentation.md` — documentation phase index