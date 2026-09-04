import sqlite3

from src.sql_analysis.database import DATABASE_PATH


def main() -> None:
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"Database not found: {DATABASE_PATH}"
        )

    with sqlite3.connect(DATABASE_PATH) as connection:
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


if __name__ == "__main__":
    main()
