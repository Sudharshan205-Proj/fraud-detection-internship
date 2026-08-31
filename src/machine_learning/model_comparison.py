"""
Model comparison utilities for the Fraud Detection System.

Phase 8:
Compare supervised classification and anomaly-detection models
using fraud-detection-focused evaluation metrics.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

REQUIRED_COLUMNS = {
    "model",
    "accuracy",
    "precision",
    "recall",
    "f1_score",
    "roc_auc",
}


def create_model_comparison(results: list[dict]) -> pd.DataFrame:
    """
    Convert model result dictionaries into a comparison DataFrame.

    Parameters
    ----------
    results:
        List of dictionaries containing model evaluation metrics.

    Returns
    -------
    pandas.DataFrame
        Model comparison table.
    """
    if not results:
        raise ValueError("At least one model result is required.")

    df = pd.DataFrame(results)

    missing_columns = REQUIRED_COLUMNS - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    return df.sort_values(
        by="f1_score",
        ascending=False,
    ).reset_index(drop=True)


def select_best_model(
    comparison_df: pd.DataFrame,
    metric: str = "f1_score",
) -> str:
    """
    Select the model with the highest value for the chosen metric.

    F1-score is used by default because fraud detection requires
    a balance between precision and recall.
    """
    if comparison_df.empty:
        raise ValueError("Comparison DataFrame cannot be empty.")

    if metric not in comparison_df.columns:
        raise ValueError(f"Metric '{metric}' not found in comparison data.")

    best_row = comparison_df.loc[
        comparison_df[metric].idxmax()
    ]

    return str(best_row["model"])


def save_comparison_table(
    comparison_df: pd.DataFrame,
    output_path: str | Path,
) -> None:
    """
    Save the model comparison table as CSV.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    comparison_df.to_csv(
        output_path,
        index=False,
    )


def plot_model_comparison(
    comparison_df: pd.DataFrame,
    output_path: str | Path,
) -> None:
    """
    Create a comparison chart for the main fraud-detection metrics.
    """
    metrics = [
        "precision",
        "recall",
        "f1_score",
        "roc_auc",
    ]

    plot_df = comparison_df.set_index("model")[metrics]

    ax = plot_df.plot(
        kind="bar",
        figsize=(12, 6),
    )

    ax.set_title("Fraud Detection Model Comparison")
    ax.set_xlabel("Model")
    ax.set_ylabel("Score")
    ax.set_ylim(0, 1.05)

    plt.xticks(rotation=20)
    plt.tight_layout()

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.savefig(
        output_path,
        dpi=150,
        bbox_inches="tight",
    )

    plt.close()
