from src.machine_learning.model_comparison import (
    create_model_comparison,
    plot_model_comparison,
    save_comparison_table,
    select_best_model,
)

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
]


comparison = create_model_comparison(results)

print("\nModel Comparison")
print("=" * 70)
print(comparison.to_string(index=False))

best_model = select_best_model(comparison)

print("\nSelected primary model:", best_model)


save_comparison_table(
    comparison,
    "docs/machine-learning/model-comparison.csv",
)

plot_model_comparison(
    comparison,
    "docs/machine-learning/model-comparison.png",
)

print("\nComparison table saved.")
print("Comparison chart saved.")
