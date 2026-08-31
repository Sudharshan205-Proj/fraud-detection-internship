import pandas as pd

from src.machine_learning.evaluation import evaluate_model
from src.machine_learning.models import (
    create_logistic_regression,
    create_random_forest,
    train_model,
)
from src.machine_learning.prepare import (
    prepare_categorical_features,
    split_features_target,
    train_test_split_data,
)

DATA_PATH = "data/processed/paysim_processed.csv"


def prepare_data():
    """
    Load and prepare the processed PaySim dataset.
    """
    df = pd.read_csv(DATA_PATH)

    X, y = split_features_target(df)

    X = prepare_categorical_features(X)

    X_train, X_test, y_train, y_test = train_test_split_data(
        X,
        y,
        test_size=0.2,
    )

    return X_train, X_test, y_train, y_test


def run_baseline_models():
    """
    Train and evaluate baseline classification models.
    """
    X_train, X_test, y_train, y_test = prepare_data()

    models = {
        "Logistic Regression": create_logistic_regression(),
        "Random Forest": create_random_forest(),
    }

    results = {}

    for name, model in models.items():
        print(f"\nTraining {name}...")

        trained_model = train_model(
            model,
            X_train,
            y_train,
        )

        metrics = evaluate_model(
            trained_model,
            X_test,
            y_test,
        )

        results[name] = metrics

        print(f"\n{name} Results")

        for metric, value in metrics.items():
            print(f"{metric}: {value:.6f}")

    return results


if __name__ == "__main__":
    run_baseline_models()
