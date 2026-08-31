"""
Generate held-out Random Forest predictions for Phase 7 threshold analysis.
"""

from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from src.machine_learning.prepare import (
    prepare_categorical_features,
    split_features_target,
    train_test_split_data,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "paysim_processed.csv"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "docs"
    / "machine-learning"
    / "random-forest-predictions.csv"
)


def main() -> None:
    print("Loading processed dataset...")

    df = pd.read_csv(DATA_PATH)

    X, y = split_features_target(df)

    X = prepare_categorical_features(X)

    X_train, X_test, y_train, y_test = train_test_split_data(
        X,
        y,
        test_size=0.2,
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        n_jobs=-1,
        class_weight="balanced",
    )

    print("Training Random Forest...")

    model.fit(X_train, y_train)

    probabilities = model.predict_proba(X_test)[:, 1]

    predictions = pd.DataFrame(
        {
            "actual": y_test.to_numpy(),
            "probability": probabilities,
        }
    )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    predictions.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print("Prediction generation complete.")
    print(f"Rows: {len(predictions):,}")
    print(
        "Fraudulent test observations:",
        int(predictions["actual"].sum()),
    )
    print(
        "Saved to:",
        OUTPUT_PATH.relative_to(PROJECT_ROOT),
    )


if __name__ == "__main__":
    main()
