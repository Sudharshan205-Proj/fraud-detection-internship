from pathlib import Path

import pandas as pd  # noqa: F401

from src.machine_learning.model_comparison import (
    create_model_comparison,
    plot_model_comparison,
    save_comparison_table,
    select_best_model,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]

OUTPUT_DIR = PROJECT_ROOT / "results" / "model_comparison"

CSV_OUTPUT = OUTPUT_DIR / "model_comparison.csv"
PLOT_OUTPUT = OUTPUT_DIR / "model_comparison.png"
REPORT_OUTPUT = OUTPUT_DIR / "model_selection.md"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Results obtained from the verified Phase 6 and Phase 7 runs.
    results = [
        {
            "model": "Logistic Regression",
            "accuracy": 0.967201,
            "precision": 0.034137,
            "recall": 0.894096,
            "f1_score": 0.065762,
            "roc_auc": 0.984229,
        },
        {
            "model": "Random Forest",
            "accuracy": 0.999995,
            "precision": 0.998781,
            "recall": 0.997565,
            "f1_score": 0.998173,
            "roc_auc": 0.999087,
        },
        {
            "model": "Isolation Forest",
            "accuracy": None,
            "precision": 0.035260,
            "recall": 0.270237,
            "f1_score": 0.062381,
            "roc_auc": 0.893615,
        },
        {
            "model": "Autoencoder",
            "accuracy": None,
            "precision": 0.085778,
            "recall": 0.722459,
            "f1_score": 0.153349,
            "roc_auc": 0.943997,
        },
    ]

    comparison = create_model_comparison(results)

    save_comparison_table(
        comparison,
        CSV_OUTPUT,
    )

    plot_model_comparison(
        comparison,
        PLOT_OUTPUT,
    )

    best_by_f1 = select_best_model(
        comparison,
        metric="f1_score",
    )

    best_by_recall = select_best_model(
        comparison,
        metric="recall",
    )

    best_by_precision = select_best_model(
        comparison,
        metric="precision",
    )

    report = """# Phase 8 — Model Comparison and Selection

## Model Comparison

| Model | Precision | Recall | F1-score | ROC-AUC |
|---|---:|---:|---:|---:|
"""

    for _, row in comparison.iterrows():
        report += (
            f"| {row['model']} | "
            f"{row['precision']:.6f} | "
            f"{row['recall']:.6f} | "
            f"{row['f1_score']:.6f} | "
            f"{row['roc_auc']:.6f} |\n"
        )

    report += f"""
## Model Selection

### Best F1-score

**{best_by_f1}**

### Best Recall

**{best_by_recall}**

### Best Precision

**{best_by_precision}**

## Interpretation

Logistic Regression provides high recall but very low precision,
meaning that it identifies many fraudulent transactions but also
produces a large number of false positives.

Isolation Forest provides lower recall and F1-score than the
supervised approaches and produces a relatively large number of
false positives.

The Autoencoder provides substantially higher recall than Isolation
Forest and a higher F1-score, demonstrating useful anomaly-detection
capability. However, its precision remains considerably lower than
the Random Forest classifier.

Random Forest provides the strongest overall balance between
precision and recall and achieves the highest F1-score and ROC-AUC
among the evaluated approaches.

## Selection Decision

**Random Forest is selected as the primary fraud-classification model
for the application stage.**

The anomaly-detection approaches remain important supporting methods
because they demonstrate unsupervised/deep-learning approaches and
provide alternative mechanisms for identifying unusual transactions.

## Important Limitation

The reported performance is based on the current PaySim evaluation
pipeline. The exceptionally high Random Forest performance should be
interpreted carefully and investigated for potential dataset-specific
patterns, feature leakage, or unusually strong engineered features
before treating the model as production-ready.
"""

    REPORT_OUTPUT.write_text(
        report,
        encoding="utf-8",
    )

    print("\nPhase 8 Model Comparison")
    print("=" * 60)
    print(comparison.to_string(index=False))
    print("=" * 60)

    print(f"\nBest model by F1-score: {best_by_f1}")
    print(f"Best model by Recall: {best_by_recall}")
    print(f"Best model by Precision: {best_by_precision}")

    print("\nArtifacts created:")
    print(f"- {CSV_OUTPUT}")
    print(f"- {PLOT_OUTPUT}")
    print(f"- {REPORT_OUTPUT}")


if __name__ == "__main__":
    main()
