import pandas as pd
import pytest
from sklearn.ensemble import RandomForestClassifier

from src.machine_learning.explainability import (
    calculate_permutation_importance,
    get_feature_importance,
    plot_feature_importance,
    save_feature_importance,
)


def create_sample_model():
    X = pd.DataFrame(
        {
            "amount": [10, 20, 30, 100, 200, 300],
            "balance": [100, 90, 80, 500, 400, 300],
            "step": [1, 2, 3, 4, 5, 6],
        }
    )

    y = [0, 0, 0, 1, 1, 1]

    model = RandomForestClassifier(
        n_estimators=10,
        random_state=42,
    )

    model.fit(X, y)

    return model, X, pd.Series(y)


def test_feature_importance():
    model, X, _ = create_sample_model()

    result = get_feature_importance(
        model,
        X.columns,
    )

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 3
    assert list(result.columns) == [
        "feature",
        "importance",
    ]


def test_feature_importance_sorted():
    model, X, _ = create_sample_model()

    result = get_feature_importance(
        model,
        X.columns,
    )

    assert result["importance"].is_monotonic_decreasing


def test_invalid_model_raises_error():
    with pytest.raises(ValueError):
        get_feature_importance(
            object(),
            ["amount"],
        )


def test_feature_name_mismatch_raises_error():
    model, _, _ = create_sample_model()

    with pytest.raises(ValueError):
        get_feature_importance(
            model,
            ["amount"],
        )


def test_permutation_importance():
    model, X, y = create_sample_model()

    result = calculate_permutation_importance(
        model,
        X,
        y,
        n_repeats=2,
    )

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 3
    assert "feature" in result.columns
    assert "importance_mean" in result.columns
    assert "importance_std" in result.columns


def test_save_feature_importance(tmp_path):
    model, X, _ = create_sample_model()

    importance = get_feature_importance(
        model,
        X.columns,
    )

    output_file = tmp_path / "importance.csv"

    save_feature_importance(
        importance,
        output_file,
    )

    assert output_file.exists()


def test_plot_feature_importance(tmp_path):
    model, X, _ = create_sample_model()

    importance = get_feature_importance(
        model,
        X.columns,
    )

    output_file = tmp_path / "importance.png"

    plot_feature_importance(
        importance,
        output_file,
    )

    assert output_file.exists()
