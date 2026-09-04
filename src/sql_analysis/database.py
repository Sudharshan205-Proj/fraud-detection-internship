"""
SQLite database helpers for the PaySim processed dataset.
"""

import sqlite3

import pandas as pd

from src.data_processing.process_data import (
    PROCESSED_DIR,
    PROCESSED_PATH,
)

DATABASE_PATH = PROCESSED_DIR.parent / "paysim.db"

# Rows imported into SQLite per chunk so the 6.3M-row CSV never has to
# be materialised as a single in-memory pandas frame during import.
CHUNK_SIZE = 100_000


def create_database() -> None:
    """
    Create the SQLite ``transactions`` table from the processed CSV.

    The CSV is streamed in chunks of :data:`CHUNK_SIZE` rows and each
    chunk is appended to the table, keeping peak memory bounded.
    """

    if not PROCESSED_PATH.exists():
        raise FileNotFoundError(
            f"Processed dataset not found: {PROCESSED_PATH}"
        )

    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DATABASE_PATH) as connection:

        csv_reader = pd.read_csv(
            PROCESSED_PATH,
            chunksize=CHUNK_SIZE,
        )

        first_chunk = next(csv_reader)

        first_chunk.to_sql(
            "transactions",
            connection,
            if_exists="replace",
            index=False,
        )

        for chunk in csv_reader:
            chunk.to_sql(
                "transactions",
                connection,
                if_exists="append",
                index=False,
            )


def run_query(connection: sqlite3.Connection, query: str) -> pd.DataFrame:
    """
    Execute a SQL query using an existing SQLite connection.

    Parameters
    ----------
    connection : sqlite3.Connection
        Active SQLite database connection.

    query : str
        SQL query to execute.

    Returns
    -------
    pandas.DataFrame
        Query results.
    """

    return pd.read_sql_query(query, connection)


def get_connection() -> sqlite3.Connection:
    """
    Return a connection to the PaySim SQLite database.

    The caller is responsible for closing the returned connection.
    """

    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"SQLite database not found: {DATABASE_PATH}"
        )

    return sqlite3.connect(DATABASE_PATH)


if __name__ == "__main__":
    create_database()
    print(f"SQLite database successfully created: {DATABASE_PATH}")
