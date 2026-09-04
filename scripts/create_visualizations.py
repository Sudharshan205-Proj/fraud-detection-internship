"""
Create Phase 11 static visualizations.

The charts are generated from compact aggregated datasets created by
generate_visualization_data.py.

Outputs are saved to:

reports/figures/
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

DATA_DIR = Path("data/visualization")
OUTPUT_DIR = Path("reports/figures")


def save_figure(filename: str) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / filename,
        dpi=200,
        bbox_inches="tight",
    )
    plt.close()


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    summary = pd.read_csv(
        DATA_DIR / "fraud_summary.csv"
    )

    by_type = pd.read_csv(
        DATA_DIR / "fraud_by_type.csv"
    )

    by_step = pd.read_csv(
        DATA_DIR / "fraud_by_step.csv"
    )

    by_amount = pd.read_csv(
        DATA_DIR / "fraud_by_amount.csv"
    )

    model_performance = pd.read_csv(
        DATA_DIR / "model_performance.csv"
    )

    # ---------------------------------------------------------
    # 1. Fraud vs legitimate distribution
    # ---------------------------------------------------------

    fraud_value = summary.loc[
        summary["metric"] == "Fraud Transactions",
        "value",
    ].iloc[0]

    legitimate_value = summary.loc[
        summary["metric"] == "Legitimate Transactions",
        "value",
    ].iloc[0]

    labels = ["Legitimate", "Fraud"]
    values = [legitimate_value, fraud_value]

    plt.figure(figsize=(8, 5))
    plt.bar(labels, values)
    plt.title("Fraud vs Legitimate Transactions")
    plt.xlabel("Transaction Classification")
    plt.ylabel("Number of Transactions")
    plt.yscale("log")
    save_figure("fraud_distribution.png")

    # ---------------------------------------------------------
    # 2. Fraud rate by transaction type
    # ---------------------------------------------------------

    plt.figure(figsize=(9, 5))

    plt.bar(
        by_type["transaction_type"],
        by_type["fraud_rate_percent"],
    )

    plt.title("Fraud Rate by Transaction Type")
    plt.xlabel("Transaction Type")
    plt.ylabel("Fraud Rate (%)")
    plt.xticks(rotation=30)
    save_figure("fraud_by_type.png")

    # ---------------------------------------------------------
    # 3. Fraud transactions over simulation steps
    # ---------------------------------------------------------

    plt.figure(figsize=(10, 5))

    plt.plot(
        by_step["step"],
        by_step["fraud_transactions"],
    )

    plt.title("Fraud Transactions Across Simulation Steps")
    plt.xlabel("Simulation Step")
    plt.ylabel("Fraud Transactions")
    save_figure("fraud_by_step.png")

    # ---------------------------------------------------------
    # 4. Transaction amount distribution
    # ---------------------------------------------------------

    plt.figure(figsize=(11, 5))

    x = range(len(by_amount))

    plt.bar(
        x,
        by_amount["total_transactions"],
    )

    plt.title("Transactions by Amount Range")
    plt.xlabel("Transaction Amount Range")
    plt.ylabel("Number of Transactions")
    plt.xticks(
        list(x),
        by_amount["amount_bin"],
        rotation=45,
        ha="right",
    )
    plt.yscale("log")
    save_figure("fraud_by_amount.png")

    # ---------------------------------------------------------
    # 5. Model performance comparison
    # ---------------------------------------------------------

    metrics = [
        "precision",
        "recall",
        "f1_score",
        "roc_auc",
    ]

    available_metrics = [
        metric
        for metric in metrics
        if metric in model_performance.columns
    ]

    plot_data = model_performance[
        ["model"] + available_metrics
    ].copy()

    plot_data = plot_data.set_index("model")

    ax = plot_data.plot(
        kind="bar",
        figsize=(12, 6),
    )

    ax.set_title("Fraud Detection Model Performance")
    ax.set_xlabel("Model")
    ax.set_ylabel("Score")
    ax.set_ylim(0, 1.05)
    plt.xticks(rotation=20)
    plt.legend(
        title="Metric",
        bbox_to_anchor=(1.02, 1),
        loc="upper left",
    )

    save_figure("model_performance.png")

    print("=" * 70)
    print("PHASE 11 PYTHON VISUALIZATIONS COMPLETE")
    print("=" * 70)
    print()
    print("Generated figures:")
    print("  reports/figures/fraud_distribution.png")
    print("  reports/figures/fraud_by_type.png")
    print("  reports/figures/fraud_by_step.png")
    print("  reports/figures/fraud_by_amount.png")
    print("  reports/figures/model_performance.png")


if __name__ == "__main__":
    main()
