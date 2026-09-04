"""
Shared synthetic PaySim data builders for dataset-free tests.

The full PaySim dataset (6.3M rows) is gitignored and absent in CI or
fresh checkouts, so end-to-end tests generate small, deterministic,
PaySim-style frames here.
"""

import pandas as pd

from src.data_processing.process_data import (
    EXPECTED_COLUMNS,
    process_dataset,
)

TRANSACTION_TYPES = [
    "PAYMENT",
    "CASH_IN",
    "DEBIT",
    "TRANSFER",
    "CASH_OUT",
]


def make_synthetic_raw_rows(n_rows: int) -> list[dict]:
    """
    Build ``n_rows`` deterministic PaySim-style transaction records.

    Legitimate rows keep consistent balances (``oldbalanceOrig``
    minus ``amount`` equals ``newbalanceOrig``). Every 10th row is
    fraudulent with zero origin balances, alternating between
    TRANSFER and CASH_OUT, mirroring the known PaySim fraud pattern.
    """
    fraud_types = ["TRANSFER", "CASH_OUT"]
    rows = []

    for i in range(n_rows):
        # Because the normal type cycle is length 5, the fraudulent rows
        # (every 10th) would otherwise land on PAYMENT.
        fraudulent = i % 10 == 0
        transaction_type = (
            fraud_types[(i // 10) % 2]
            if fraudulent
            else TRANSACTION_TYPES[i % len(TRANSACTION_TYPES)]
        )

        amount = float(100 * (i + 1))

        if fraudulent:
            # Fraud pattern: money leaves a zero-balance origin.
            oldbalance_org = 0.0
            newbalance_org = 0.0
        else:
            oldbalance_org = float(1000 * (i + 1))
            newbalance_org = oldbalance_org - amount

        oldbalance_dest = float(500 * (i + 1))
        newbalance_dest = oldbalance_dest + amount

        rows.append(
            {
                "step": (i % 24) + 1,
                "type": transaction_type,
                "amount": amount,
                "nameOrig": f"C{i:06d}",
                "oldbalanceOrg": oldbalance_org,
                "newbalanceOrig": newbalance_org,
                "nameDest": f"D{i:06d}",
                "oldbalanceDest": oldbalance_dest,
                "newbalanceDest": newbalance_dest,
                "isFraud": int(fraudulent),
                "isFlaggedFraud": 0,
            }
        )

    return rows


def make_processed_frame(n_rows: int) -> pd.DataFrame:
    """
    Build a processed PaySim-style frame (24 columns) by running the
    canonical processing pipeline over synthetic raw rows.
    """
    raw = pd.DataFrame(
        make_synthetic_raw_rows(n_rows),
        columns=EXPECTED_COLUMNS,
    )

    return process_dataset(raw)
