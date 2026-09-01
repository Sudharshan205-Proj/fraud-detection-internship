import sqlite3
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "data" / "processed" / "paysim_processed.csv"
DATABASE_PATH = PROJECT_ROOT / "data" / "paysim.db"

CHUNK_SIZE = 100_000


def create_database() -> None:
    """Create the SQLite database from the processed PaySim dataset."""

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Processed dataset not found: {DATA_PATH}"
        )

    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DATABASE_PATH) as connection:

        csv_reader = pd.read_csv(
            DATA_PATH,
            chunksize=CHUNK_SIZE
        )

        first_chunk = next(csv_reader)

        first_chunk.to_sql(
            "transactions",
            connection,
            if_exists="replace",
            index=False
        )

        for chunk in csv_reader:
            chunk.to_sql(
                "transactions",
                connection,
                if_exists="append",
                index=False
            )


def run_query(connection, query: str):
    """Execute a SQL query using an existing SQLite connection.

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
    """Execute a SQL query against the PaySim SQLite database.

    Parameters
    ----------
    query : str
        SQL query to execute.

    Returns
    -------
    pandas.DataFrame
        Query results.
    """

    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"SQLite database not found: {DATABASE_PATH}"
        )

    with sqlite3.connect(DATABASE_PATH) as connection:  # noqa: PLR1704
        return pd.read_sql_query(query, connection)


def get_connection():
    """Return a connection to the PaySim SQLite database."""

    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"SQLite database not found: {DATABASE_PATH}"
        )

    return sqlite3.connect(DATABASE_PATH)


if __name__ == "__main__":
    create_database()
    print(f"SQLite database successfully created: {DATABASE_PATH}")
