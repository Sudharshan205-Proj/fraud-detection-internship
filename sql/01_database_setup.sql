DROP TABLE IF EXISTS transactions;

CREATE TABLE
    transactions (
        step INTEGER,
        type TEXT,
        amount REAL,
        oldbalanceOrg REAL,
        newbalanceOrig REAL,
        oldbalanceDest REAL,
        newbalanceDest REAL,
        isFraud INTEGER,
        isFlaggedFraud INTEGER,
        origin_balance_change REAL,
        destination_balance_change REAL,
        origin_balance_error REAL,
        destination_balance_error REAL,
        origin_balance_error_abs REAL,
        destination_balance_error_abs REAL,
        origin_zero_balance_before INTEGER,
        origin_zero_balance_after INTEGER,
        destination_zero_balance_before INTEGER,
        destination_zero_balance_after INTEGER,
        amount_to_origin_balance REAL,
        amount_to_destination_balance REAL,
        is_transfer INTEGER,
        is_cash_out INTEGER,
        log_amount REAL
    );