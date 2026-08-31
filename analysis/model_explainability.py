"""
Phase 9 - Random Forest model explainability analysis.
"""

from pathlib import Path

import pandas as pd

from src.machine_learning.explainability import (
    get_feature_importance,
    plot_feature_importance,
    save_feature_importance,
)

DATA_PATH = Path(
    "data/processed/paysim_processed.csv"
)

OUTPUT_DIR = Path(
    "docs/machine-learning/explainability"
)


def main():
    print("Loading processed dataset...")

    df = pd.read_csv(DATA_PATH)

    print("Rows:", len(df))
    print("Columns:", len(df.columns))

    target = "isFraud"

    X = df.drop(columns=[target])
    y = df[target]

    # Remove columns that should not be supplied directly
    # to the model if they are still present.
    identifier_columns = [
        "nameOrig",
        "nameDest",
    ]

    existing_identifiers = [
        column
        for column in identifier_columns
        if column in X.columns
    ]

    X = X.drop(
        columns=existing_identifiers,
        errors="ignore",
    )

    # One-hot encode categorical variables.
    X = pd.get_dummies(
        X,
        columns=["type"],
        dtype=int,
    )

    print("Prepared features:", X.shape[1])

    print("\nTraining Random Forest for explainability...")

    from sklearn.ensemble import RandomForestClassifier

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        n_jobs=-1,
        class_weight="balanced",
    )

    model.fit(X, y)

    print("Model trained successfully.")

    feature_importance = get_feature_importance(
        model,
        X.columns,
    )

    print("\nTop 15 Features")
    print("=" * 60)
    print(
        feature_importance.head(15).to_string(
            index=False
        )
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    csv_path = (
        OUTPUT_DIR
        / "random-forest-feature-importance.csv"
    )

    image_path = (
        OUTPUT_DIR
        / "random-forest-feature-importance.png"
    )

    save_feature_importance(
        feature_importance,
        csv_path,
    )

    plot_feature_importance(
        feature_importance,
        image_path,
        top_n=15,
    )

    print("\nFeature importance saved:")
    print(csv_path)

    print("\nFeature importance chart saved:")
    print(image_path)


if __name__ == "__main__":
    main()
