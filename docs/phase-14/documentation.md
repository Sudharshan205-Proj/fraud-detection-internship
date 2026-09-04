# Phase 14 — Documentation

## Objective

Ensure the repository is fully and consistently documented: setup,
running, testing, architecture, per-phase reports, and the internship
curriculum evidence.

## Status

**In progress** — this documentation set is being completed now. The
README, architecture, testing, and final-report documents exist; the
per-phase report set is the current work item.

## Documentation Inventory

| Location | Contents |
|---|---|
| `README.md` | Project overview, terminology (24/36/33 columns), setup, run commands, testing, docs index, phase status |
| `docs/architecture.md` | Repository layout, package responsibilities, data flow, artifact conventions |
| `docs/testing.md` | Test layout and how to extend the suite |
| `docs/phase-0/` | Project requirements + curriculum mapping |
| `docs/phase-1/` … `docs/phase-16/` | Per-phase reports (objective, deliverables, commands, status) |
| `docs/data/` | Dataset, data dictionary, data quality, processing reports |
| `docs/sql/` | SQL analysis workflow |
| `docs/machine-learning/` | ML preparation, baselines, evaluation, leakage, selection, explainability |
| `docs/anomaly-detection/` | Anomaly-detection report |
| `docs/final/` | Final case-study reports (overview, methodology, results, ethics, limitations) |

## Conventions

- **Column terminology is fixed**: processed = 24 columns, feature
  engineered = 36 columns, model features = 33.
- **Phase numbering is canonical**: the README project-status table is
  the source of truth (e.g. Phase 6 = supervised ML including threshold
  optimization; Phase 7 = anomaly detection; Phase 8 = comparison;
  Phase 9 = explainability).
- Phase reports cross-link the topical docs instead of duplicating their
  content; result tables live in the topical documents.

## Related Documentation

- `README.md` — index of this documentation set
- `docs/architecture.md` — layout conventions
- `docs/phase-0/curriculum-mapping.md` — the curriculum evidence matrix
  this phase supports