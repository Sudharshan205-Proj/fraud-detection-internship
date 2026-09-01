import sqlite3
from pathlib import Path

database_path = Path("data/paysim.db")

if not database_path.exists():
    raise FileNotFoundError(f"Database not found: {database_path}")

with sqlite3.connect(database_path) as connection:
    tables = connection.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        """
    ).fetchall()

    print("Tables:")
    for table in tables:
        print(f"- {table[0]}")

    count = connection.execute(
        "SELECT COUNT(*) FROM transactions"
    ).fetchone()[0]

    fraud_count = connection.execute(
        "SELECT COUNT(*) FROM transactions WHERE isFraud = 1"
    ).fetchone()[0]

    print(f"\nTransaction rows: {count:,}")
    print(f"Fraudulent rows: {fraud_count:,}")
