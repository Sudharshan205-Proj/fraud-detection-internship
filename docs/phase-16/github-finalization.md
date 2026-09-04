# Phase 16 — GitHub Finalization

## Objective

Prepare the repository for final submission: clean history, complete
documentation, reproducible environment, and a verified curriculum
audit.

## Status

**Pending** — matches the project-status table in the README. This
document is the finalization checklist.

## Checklist

- [ ] **Repository hygiene** — no large or raw artifacts committed:
  `data/raw/`, `data/processed/`, and `models/` stay gitignored; the
  dataset is documented as a local download.
- [ ] **No secrets** — confirm no credentials, keys, or personal data in
  tracked files (the PaySim identifiers are synthetic and were already
  removed from the processed dataset).
- [ ] **Notebooks** — outputs stripped, notebooks validate under
  `nbformat`.
- [ ] **Environment** — `requirements.txt` (pinned, UTF-8) and
  `pyproject.toml` committed; `pip install -e .` works from a clean
  clone.
- [ ] **README** — setup, dataset placement, run commands, testing, and
  documentation index complete.
- [ ] **Tests** — full suite green (`python -m pytest`), no
  `PYTHONPATH` hacks required.
- [ ] **Application files** — `app/`, `models/` artifacts, and
  `tests/app/` committed once Phase 10 wiring is complete.
- [ ] **Curriculum audit** — every row of the evidence matrix in
  `docs/phase-0/curriculum-mapping.md` resolved (🟩/📄/❌ with reasons),
  with no unexplained gaps (per §15 of that document).
- [ ] **Final review** — `git diff` review for accidental changes; final
  commit with a descriptive message; push to GitHub; open the final
  internship-submission PR if required.

## Related Documentation

- `docs/phase-0/curriculum-mapping.md` — final compliance rule (§15)
- `docs/phase-14/documentation.md` — documentation completeness
- `README.md` — the repository's entry point