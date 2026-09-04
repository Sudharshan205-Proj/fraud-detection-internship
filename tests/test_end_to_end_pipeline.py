"""
Dataset-free end-to-end smoke test.

Generates a small synthetic PaySim-style raw CSV, runs the complete
processing pipeline (load -> validate -> engineer -> save), reloads the
resulting processed file, asserts the documented 24-column layout, and
then runs the model-preparation flow (target split, categorical
encoding, stratified split, training, evaluation) on the processed
data.

Nothing in this test touches the real ``data/`` directory: all files
are written under pytest's ``tmp_path``.
"""

import numpy as np
import pandas as pd
import pytest

from src.data_processing.process_data import (
    ENGINEERED_COLUMNS,
    EXPECTED_COLUMNS,
    PROCESSED_COLUMNS,
    load_data,
    load_processed_dataset,
    process_dataset,
    validate_raw_data,
)
from src.machine_learning.evaluation import evaluate_model
from src.machine_learning.models import (
    create_random_forest,
    train_model,
)
from src.machine_learning.prepare import (
    prepare_categorical_features,
    split_features_target,
    train_test_split_data,
)
from tests.helpers import make_synthetic_raw_rows

TARGET_COLUMN = "isFraud"


def _write_raw_csv(rows: list[dict], path) -> None:
    df = pd.DataFrame(rows, columns=EXPECTED_COLUMNS)
    df.to_csv(path, index=False)


@pytest.fixture
def synthetic_raw_path(tmp_path):
    path = tmp_path / "raw_paysim.csv"
    _write_raw_csv(make_synthetic_raw_rows(80), path)
    return path


def test_end_to_end_processing_and_model_preparation(
    synthetic_raw_path,
    tmp_path,
):
    # ------------------------------------------------------------------
    # Stage 1: processing pipeline (mirrors src.data_processing main()).
    # ------------------------------------------------------------------

    raw = load_data(synthetic_raw_path)

    assert len(raw) == 80
    assert list(raw.columns) == EXPECTED_COLUMNS

    validate_raw_data(raw)

    processed = process_dataset(raw)

    processed_path = tmp_path / "paysim_processed.csv"
    processed.to_csv(processed_path, index=False)

    # ------------------------------------------------------------------
    # Stage 2: processed-file layout assertions.
    # ------------------------------------------------------------------

    reloaded = load_processed_dataset(processed_path)

    assert list(reloaded.columns) == PROCESSED_COLUMNS
    assert len(PROCESSED_COLUMNS) == 24
    assert len(ENGINEERED_COLUMNS) == 15
    assert len(reloaded) == len(raw)

    # Identifiers are removed; the target and flag are preserved.
    assert "nameOrig" not in reloaded.columns
    assert "nameDest" not in reloaded.columns
    assert TARGET_COLUMN in reloaded.columns
    assert "isFlaggedFraud" in reloaded.columns

    # Dtype-aware layout: money stays float64, indicators are small ints,
    # derived log/ratio features are float32.
    assert reloaded["amount"].dtype == np.dtype("float64")
    assert reloaded[TARGET_COLUMN].dtype.name == "int8"
    assert reloaded["is_transfer"].dtype.name == "int8"
    assert reloaded["log_amount"].dtype.name == "float32"
    assert reloaded["step"].dtype.name == "int16"

    # Balance consistency for a legitimate row: origin balance change
    # must equal the transaction amount (error of exactly zero).
    legitimate = reloaded[reloaded[TARGET_COLUMN] == 0].iloc[0]
    assert legitimate["origin_balance_error"] == 0.0
    assert legitimate["destination_balance_error"] == 0.0

    # Engineered rows must contain no missing or infinite values.
    numeric = reloaded.select_dtypes(include="number")
    assert not numeric.isna().any().any()
    assert np.isfinite(numeric.to_numpy()).all()

    # ------------------------------------------------------------------
    # Stage 3: model-preparation flow on the processed file.
    # ------------------------------------------------------------------

    X, y = split_features_target(reloaded)

    assert TARGET_COLUMN not in X.columns
    assert y.name == TARGET_COLUMN
    assert len(X) == len(y)

    X_prepared = prepare_categorical_features(X)

    # One-hot encoded transaction types replace the raw type column.
    assert "type" not in X_prepared.columns
    assert "type_TRANSFER" in X_prepared.columns
    assert "type_CASH_OUT" in X_prepared.columns
    assert len(X_prepared.columns) == len(X.columns) + 4

    X_train, X_test, y_train, y_test = train_test_split_data(
        X_prepared,
        y,
        test_size=0.25,
    )

    # Stratified split keeps both classes present in train and test.
    assert y_train.nunique() == 2
    assert y_test.nunique() == 2

    model = train_model(
        create_random_forest(),
        X_train,
        y_train,
    )

    metrics = evaluate_model(model, X_test, y_test)

    required_metrics = {
        "accuracy",
        "precision",
        "recall",
        "f1_score",
        "roc_auc",
    }

    assert required_metrics.issubset(metrics.keys())

    for value in metrics.values():
        assert 0.0 <= value <= 1.0


def test_e2e_fraud_rows_are_present_in_sample(synthetic_raw_path):
    raw = load_data(synthetic_raw_path)

    fraud_count = int(raw[TARGET_COLUMN].sum())

    # Roughly every 10th TRANSFER/CASH_OUT row is fraudulent: expect
    # 8 of the 80 rows.
    assert fraud_count == 8
