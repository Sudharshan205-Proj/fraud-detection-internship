"""
Generate compact datasets for Phase 11 visualizations and Tableau.

The project dataset contains more than six million transactions, so this
script does not create another copy of the transaction-level dataset.

Instead, it reads the processed PaySim dataset in chunks and produces
small aggregated datasets suitable for:

- Python visualizations
- R analysis
- R Markdown
- Tableau Public

Source:
    data/processed/paysim_processed.csv

Outputs:
    data/visualization/fraud_dashboard_data.csv
    data/visualization/fraud_summary.csv
    data/visualization/fraud_by_type.csv
    data/visualization/fraud_by_step.csv
    data/visualization/fraud_by_amount.csv
    data/visualization/model_performance.csv
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import pandas as pd

DATA_PATH = Path("data/processed/paysim_processed.csv")
MODEL_RESULTS_PATH = Path("results/model_comparison/model_comparison.csv")
OUTPUT_DIR = Path("data/visualization")

CHUNK_SIZE = 250_000

AMOUNT_BINS = [
    -0.01,
    100,
    500,
    1_000,
    5_000,
    10_000,
    50_000,
    100_000,
    500_000,
    1_000_000,
    float("inf"),
]

AMOUNT_LABELS = [
    "0-100",
    "101-500",
    "501-1,000",
    "1,001-5,000",
    "5,001-10,000",
    "10,001-50,000",
    "50,001-100,000",
    "100,001-500,000",
    "500,001-1,000,000",
    "1,000,001+",
]


def validate_columns(columns: list[str]) -> None:
    required = {"isFraud", "type", "amount", "step"}

    missing = required.difference(columns)

    if missing:
        raise ValueError(
            "The processed dataset is missing required columns: "
            + ", ".join(sorted(missing))
        )


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Processed dataset not found: {DATA_PATH}"
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("PHASE 11 - VISUALIZATION DATA GENERATION")
    print("=" * 70)
    print(f"Input: {DATA_PATH}")
    print()

    aggregations: defaultdict[tuple, int] = defaultdict(int)

    total_transactions = 0
    total_fraud = 0
    total_amount = 0.0
    minimum_amount = float("inf")
    maximum_amount = float("-inf")

    first_chunk = True

    for chunk_number, chunk in enumerate(
        pd.read_csv(
            DATA_PATH,
            usecols=["isFraud", "type", "amount", "step"],
            chunksize=CHUNK_SIZE,
        ),
        start=1,
    ):
        if first_chunk:
            validate_columns(chunk.columns.tolist())
            first_chunk = False

        chunk["isFraud"] = pd.to_numeric(
            chunk["isFraud"], errors="coerce"
        ).fillna(0).astype(int)

        chunk["amount"] = pd.to_numeric(
            chunk["amount"], errors="coerce"
        ).fillna(0.0)

        chunk["step"] = pd.to_numeric(
            chunk["step"], errors="coerce"
        ).fillna(0).astype(int)

        chunk["fraud_status"] = chunk["isFraud"].map(
            {0: "Legitimate", 1: "Fraud"}
        )

        chunk["amount_bin"] = pd.cut(
            chunk["amount"],
            bins=AMOUNT_BINS,
            labels=AMOUNT_LABELS,
            include_lowest=True,
        ).astype(str)

        grouped = (
            chunk.groupby(
                ["type", "fraud_status", "step", "amount_bin"],
                observed=True,
            )
            .size()
            .reset_index(name="transaction_count")
        )

        for row in grouped.itertuples(index=False):
            key = (
                str(row.type),
                str(row.fraud_status),
                int(row.step),
                str(row.amount_bin),
            )

            aggregations[key] += int(row.transaction_count)

        total_transactions += len(chunk)
        total_fraud += int(chunk["isFraud"].sum())
        total_amount += float(chunk["amount"].sum())

        if len(chunk):
            minimum_amount = min(
                minimum_amount,
                float(chunk["amount"].min()),
            )
            maximum_amount = max(
                maximum_amount,
                float(chunk["amount"].max()),
            )

        print(
            f"Processed chunk {chunk_number}: "
            f"{total_transactions:,} transactions"
        )

    print()
    print("Creating visualization datasets...")

    dashboard_rows = [
        {
            "transaction_type": key[0],
            "fraud_status": key[1],
            "step": key[2],
            "amount_bin": key[3],
            "transaction_count": value,
        }
        for key, value in aggregations.items()
    ]

    dashboard = pd.DataFrame(dashboard_rows)

    if dashboard.empty:
        raise RuntimeError(
            "No visualization data was generated."
        )

    dashboard = dashboard.sort_values(
        ["step", "transaction_type", "fraud_status", "amount_bin"]
    )

    dashboard.to_csv(
        OUTPUT_DIR / "fraud_dashboard_data.csv",
        index=False,
    )

    summary = pd.DataFrame(
        [
            {
                "metric": "Total Transactions",
                "value": total_transactions,
            },
            {
                "metric": "Fraud Transactions",
                "value": total_fraud,
            },
            {
                "metric": "Legitimate Transactions",
                "value": total_transactions - total_fraud,
            },
            {
                "metric": "Fraud Rate (%)",
                "value": (
                    total_fraud / total_transactions * 100
                    if total_transactions
                    else 0
                ),
            },
            {
                "metric": "Total Transaction Amount",
                "value": total_amount,
            },
            {
                "metric": "Average Transaction Amount",
                "value": (
                    total_amount / total_transactions
                    if total_transactions
                    else 0
                ),
            },
            {
                "metric": "Minimum Transaction Amount",
                "value": minimum_amount,
            },
            {
                "metric": "Maximum Transaction Amount",
                "value": maximum_amount,
            },
        ]
    )

    summary.to_csv(
        OUTPUT_DIR / "fraud_summary.csv",
        index=False,
    )

    by_type = (
        dashboard.groupby("transaction_type", as_index=False)
        .agg(total_transactions=("transaction_count", "sum"))
    )

    fraud_by_type = (
        dashboard[dashboard["fraud_status"] == "Fraud"]
        .groupby("transaction_type")["transaction_count"]
        .sum()
        .rename("fraud_transactions")
    )

    by_type = by_type.join(fraud_by_type, on="transaction_type")
    by_type["fraud_transactions"] = (
        by_type["fraud_transactions"].fillna(0).astype(int)
    )
    by_type["fraud_rate_percent"] = (
        by_type["fraud_transactions"]
        / by_type["total_transactions"]
        * 100
    )

    by_type = by_type.sort_values(
        "fraud_rate_percent",
        ascending=False,
    )

    by_type.to_csv(
        OUTPUT_DIR / "fraud_by_type.csv",
        index=False,
    )

    by_step = (
        dashboard.groupby("step", as_index=False)
        .agg(total_transactions=("transaction_count", "sum"))
    )

    fraud_by_step = (
        dashboard[dashboard["fraud_status"] == "Fraud"]
        .groupby("step")["transaction_count"]
        .sum()
        .rename("fraud_transactions")
    )

    by_step = by_step.join(fraud_by_step, on="step")
    by_step["fraud_transactions"] = (
        by_step["fraud_transactions"].fillna(0).astype(int)
    )
    by_step["fraud_rate_percent"] = (
        by_step["fraud_transactions"]
        / by_step["total_transactions"]
        * 100
    )

    by_step = by_step.sort_values("step")

    by_step.to_csv(
        OUTPUT_DIR / "fraud_by_step.csv",
        index=False,
    )

    by_amount = (
        dashboard.groupby("amount_bin", as_index=False)
        .agg(total_transactions=("transaction_count", "sum"))
    )

    fraud_by_amount = (
        dashboard[dashboard["fraud_status"] == "Fraud"]
        .groupby("amount_bin")["transaction_count"]
        .sum()
        .rename("fraud_transactions")
    )

    by_amount = by_amount.join(
        fraud_by_amount,
        on="amount_bin",
    )

    by_amount["fraud_transactions"] = (
        by_amount["fraud_transactions"]
        .fillna(0)
        .astype(int)
    )

    by_amount["fraud_rate_percent"] = (
        by_amount["fraud_transactions"]
        / by_amount["total_transactions"]
        * 100
    )

    by_amount["amount_order"] = range(len(by_amount))

    by_amount.to_csv(
        OUTPUT_DIR / "fraud_by_amount.csv",
        index=False,
    )

    if MODEL_RESULTS_PATH.exists():
        model_performance = pd.read_csv(MODEL_RESULTS_PATH)

        model_performance.to_csv(
            OUTPUT_DIR / "model_performance.csv",
            index=False,
        )

        print(
            f"Copied model performance from: "
            f"{MODEL_RESULTS_PATH}"
        )
    else:
        print(
            "WARNING: model comparison CSV was not found. "
            "The model-performance dataset was not generated."
        )

    print()
    print("=" * 70)
    print("VISUALIZATION DATA GENERATION COMPLETE")
    print("=" * 70)
    print(f"Total transactions: {total_transactions:,}")
    print(f"Fraud transactions: {total_fraud:,}")
    print(
        f"Fraud rate: "
        f"{(total_fraud / total_transactions * 100):.4f}%"
    )
    print()
    print("Generated:")
    print("  data/visualization/fraud_dashboard_data.csv")
    print("  data/visualization/fraud_summary.csv")
    print("  data/visualization/fraud_by_type.csv")
    print("  data/visualization/fraud_by_step.csv")
    print("  data/visualization/fraud_by_amount.csv")
    print("  data/visualization/model_performance.csv")


if __name__ == "__main__":
    main()
