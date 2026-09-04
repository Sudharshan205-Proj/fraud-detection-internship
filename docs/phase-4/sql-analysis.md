# Phase 4 — SQL Analysis

## Objective

Perform relational analysis of the processed PaySim dataset using
SQLite, answering fraud-related analytical questions with SQL rather
than SQL existing only as a demonstration.

## Status

**Complete** — matches the project-status table in the README.

## What Was Produced

- **SQL analysis scripts** — `sql/`:

  - `01_database_setup.sql` — database and table creation
  - `02_basic_queries.sql` — structure and row counts
  - `03_fraud_analysis.sql` — fraud counts, rates, and fraud-by-type queries
  - `04_aggregation.sql` — sums, averages, grouped fraud rates,
    high-value transaction analysis
  - `05_joins.sql` — relational joins
  - `06_subqueries.sql` — subquery-based analysis
  - `07_temp_tables.sql` — temporary-table workflows
  - `08_validation.sql` — validation and integrity checks

- **SQLite helper module** — `src/sql_analysis/database.py`:

  - `create_database` — builds the SQLite database from the processed CSV
  - `run_query` / `get_connection` — query helpers used by the scripts
    and the inspection entry point

- **Database check script** — `scripts/check_database.py` — prints
  database diagnostics (tables, row counts, sample rows).

- **Tests** — `tests/sql/test_sql_analysis.py`.

## How to Reproduce

```bash
# Build the SQLite database from the processed CSV
python -m src.sql_analysis.database

# Inspect it
python scripts/check_database.py
```

The `sql/*.sql` files are written to run against the built database and
can also be executed interactively in DB Browser for SQLite.

## Related Documentation

- `docs/sql/sql-analysis.md` — the SQL analysis workflow and query
  documentation
- `docs/phase-1/data-processing.md` — the processed dataset the database
  is built from
- `docs/phase-5/machine-learning-preparation.md` — the next phase