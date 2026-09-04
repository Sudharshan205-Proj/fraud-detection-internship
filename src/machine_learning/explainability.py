"""
Model explainability utilities.

Phase 9:
Explain the behaviour of the selected Random Forest fraud-detection model.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.inspection import permutation_importance


def _prepare_output_path(output_path: str | Path) -> Path:
    """Create the parent directory for an output artifact."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def get_feature_importance(model, feature_names) -> pd.DataFrame:
    """
    Return Random Forest feature importance values.

    Parameters
    ----------
    model:
        Fitted tree-based model containing feature_importances_.

    feature_names:
        Names of model features.

    Returns
    -------
    pandas.DataFrame
        Features sorted by importance.
    """
    if not hasattr(model, "feature_importances_"):
        raise ValueError(
            "The supplied model does not provide feature_importances_."
        )

    if len(feature_names) != len(model.feature_importances_):
        raise ValueError(
            "Number of feature names does not match model features."
        )

    importance_df = pd.DataFrame(
        {
            "feature": feature_names,
            "importance": model.feature_importances_,
        }
    )

    return importance_df.sort_values(
        by="importance",
        ascending=False,
    ).reset_index(drop=True)


def calculate_permutation_importance(
    model,
    X,
    y,
    random_state: int = 42,
    n_repeats: int = 5,
) -> pd.DataFrame:
    """
    Calculate permutation feature importance.
    """
    result = permutation_importance(
        model,
        X,
        y,
        n_repeats=n_repeats,
        random_state=random_state,
        scoring="f1",
        n_jobs=-1,
    )

    return (
        pd.DataFrame(
            {
                "feature": X.columns,
                "importance_mean": result.importances_mean,
                "importance_std": result.importances_std,
            }
        )
        .sort_values(
            by="importance_mean",
            ascending=False,
        )
        .reset_index(drop=True)
    )


def save_feature_importance(
    importance_df: pd.DataFrame,
    output_path: str | Path,
) -> None:
    """
    Save feature importance results as CSV.
    """
    output_path = _prepare_output_path(output_path)

    importance_df.to_csv(
        output_path,
        index=False,
    )


def plot_feature_importance(
    importance_df: pd.DataFrame,
    output_path: str | Path,
    top_n: int = 15,
) -> None:
    """
    Plot the top model feature importances.
    """
    plot_df = importance_df.head(top_n).sort_values(
        by="importance",
        ascending=True,
    )

    ax = plot_df.plot(
        kind="barh",
        x="feature",
        y="importance",
        figsize=(10, 7),
        legend=False,
    )

    ax.set_title("Random Forest Feature Importance")
    ax.set_xlabel("Importance")
    ax.set_ylabel("Feature")

    plt.tight_layout()

    output_path = _prepare_output_path(output_path)

    plt.savefig(
        output_path,
        dpi=150,
        bbox_inches="tight",
    )

    plt.close()
