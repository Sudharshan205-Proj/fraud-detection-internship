import pandas as pd
import pytest

from src.machine_learning.model_comparison import (
    create_model_comparison,
    plot_model_comparison,
    save_comparison_table,
    select_best_model,
)


def sample_results():
    return [
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


def test_create_model_comparison():
    df = create_model_comparison(sample_results())

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert "model" in df.columns
    assert "f1_score" in df.columns


def test_comparison_sorted_by_f1():
    df = create_model_comparison(sample_results())

    assert df.iloc[0]["model"] == "Random Forest"
    assert df.iloc[0]["f1_score"] > df.iloc[1]["f1_score"]


def test_empty_results_raises_error():
    with pytest.raises(ValueError):
        create_model_comparison([])


def test_missing_metric_raises_error():
    bad_results = [
        {
            "model": "Test Model",
            "accuracy": 0.9,
        }
    ]

    with pytest.raises(ValueError):
        create_model_comparison(bad_results)


def test_best_model_selection():
    df = create_model_comparison(sample_results())

    best_model = select_best_model(df)

    assert best_model == "Random Forest"


def test_best_model_by_recall():
    df = create_model_comparison(sample_results())

    best_model = select_best_model(
        df,
        metric="recall",
    )

    assert best_model == "Random Forest"


def test_save_comparison_table(tmp_path):
    df = create_model_comparison(sample_results())

    output_file = tmp_path / "comparison.csv"

    save_comparison_table(
        df,
        output_file,
    )

    assert output_file.exists()

    loaded = pd.read_csv(output_file)

    assert len(loaded) == 2


def test_plot_model_comparison(tmp_path):
    df = create_model_comparison(sample_results())

    output_file = tmp_path / "comparison.png"

    plot_model_comparison(
        df,
        output_file,
    )

    assert output_file.exists()
