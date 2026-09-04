import argparse

from src.data_processing.process_data import load_processed_dataset
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


def prepare_data(max_rows: int | None = None):
    """
    Load and prepare the processed PaySim dataset.

    Parameters
    ----------
    max_rows:
        Optional cap on the number of rows loaded (sample mode).
    """
    df = load_processed_dataset(max_rows=max_rows)

    X, y = split_features_target(df)

    X = prepare_categorical_features(X)

    X_train, X_test, y_train, y_test = train_test_split_data(
        X,
        y,
        test_size=0.2,
    )

    return X_train, X_test, y_train, y_test


def run_baseline_models(max_rows: int | None = None):
    """
    Train and evaluate baseline classification models.

    Parameters
    ----------
    max_rows:
        Optional row cap passed through to the dataset loader.
    """
    if max_rows is not None:
        print(f"Sample mode active: using at most {max_rows:,} rows.")

    X_train, X_test, y_train, y_test = prepare_data(max_rows=max_rows)

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


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Train and evaluate the baseline Logistic Regression and "
            "Random Forest models on the processed PaySim dataset."
        ),
    )
    parser.add_argument(
        "--max-rows",
        type=int,
        default=None,
        metavar="N",
        help="Optional row cap for fast sample-mode runs (default: full dataset).",
    )
    args = parser.parse_args()

    run_baseline_models(max_rows=args.max_rows)


if __name__ == "__main__":
    main()
