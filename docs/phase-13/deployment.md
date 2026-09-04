# Phase 13 — Deployment

## Objective

Deploy the Phase 10 application through a simple, reproducible,
internship-level procedure so that anyone can run the fraud-detection
interface from the repository.

## Status

**Pending** — matches the project-status table in the README. Nothing
has been deployed yet; this document records the intended approach and
the reproducibility guarantees already in place.

## Reproducibility Already in Place

- `requirements.txt` — 147 pinned runtime dependencies (UTF-8)
- `pyproject.toml` — packaging (`pip install -e .` registers the `src`
  package) plus pytest configuration
- `data/` and `models/` are gitignored: the dataset is placed locally
  and the model artifacts are regenerated with
  `python -m src.machine_learning.train_final_model`
- README setup section covers environment creation and dataset placement

## Intended Deployment Approach

1. **Local run** — `.venv` + `pip install -r requirements.txt` +
   `pip install -e .`, then `python -m streamlit run app/streamlit_app.py`
   (once the Phase 10 wiring is complete).
2. **Lightweight hosting** — Streamlit Community Cloud is the natural
   candidate for a hosted demo: it runs `streamlit_app.py` directly,
   needs no server configuration, and suits the internship-level scope.
   Secrets/credentials are not part of this project.

## Explicit Non-Goals

Per `docs/phase-0/project-requirements.md` (§12), this phase will not
attempt production banking infrastructure, real-time transaction
processing, enterprise authentication, or high-availability hosting.

## Related Documentation

- `docs/phase-10/application-development.md` — the application being deployed
- `docs/phase-0/project-requirements.md` — deployment requirements and
  scope limitations
- `README.md` — setup and run instructions