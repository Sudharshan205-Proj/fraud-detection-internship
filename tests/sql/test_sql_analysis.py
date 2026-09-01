import sqlite3

import pandas as pd
import pytest

import src.sql_analysis.database


@pytest.fixture
def sample_data():
    return pd.DataFrame(
        {
            "step": [1, 2, 3, 4, 5, 6],
            "type": [
                "PAYMENT",
                "CASH_OUT",
                "TRANSFER",
                "CASH_IN",
                "DEBIT",
                "PAYMENT",
            ],
            "amount": [
                100.0,
                500.0,
                300.0,
                700.0,
                200.0,
                150.0,
            ],
            "isFraud": [0, 1, 1, 0, 0, 0],
        }
    )


@pytest.fixture
def connection(sample_data):
    conn = sqlite3.connect(":memory:")
    sample_data.to_sql(
        "transactions",
        conn,
        if_exists="replace",
        index=False,
    )

    yield conn

    conn.close()


def test_database_contains_transactions(connection):
    result = src.sql_analysis.database.run_query(
        connection,
        "SELECT COUNT(*) AS count FROM transactions",
    )

    assert result.iloc[0]["count"] == 6


def test_fraud_count(connection):
    result = src.sql_analysis.database.run_query(
        connection,
        """
        SELECT COUNT(*) AS fraud_count
        FROM transactions
        WHERE isFraud = 1
        """,
    )

    assert result.iloc[0]["fraud_count"] == 2


def test_transaction_type_grouping(connection):
    result = src.sql_analysis.database.run_query(
        connection,
        """
        SELECT type, COUNT(*) AS count
        FROM transactions
        GROUP BY type
        ORDER BY type
        """,
    )

    assert len(result) == 5


def test_average_transaction_amount(connection):
    result = src.sql_analysis.database.run_query(
        connection,
        """
        SELECT AVG(amount) AS average_amount
        FROM transactions
        """,
    )

    assert result.iloc[0]["average_amount"] > 0


def test_fraud_by_transaction_type(connection):
    result = src.sql_analysis.database.run_query(
        connection,
        """
        SELECT type, COUNT(*) AS fraud_count
        FROM transactions
        WHERE isFraud = 1
        GROUP BY type
        """,
    )

    assert result["fraud_count"].sum() == 2
