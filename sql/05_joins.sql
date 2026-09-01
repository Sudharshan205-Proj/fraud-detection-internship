-- Create transaction-type summary
DROP TABLE IF EXISTS transaction_type_summary;

CREATE TEMP
TABLE transaction_type_summary AS
SELECT
    type,
    COUNT(*) AS transaction_count,
    SUM(isFraud) AS fraudulent_transactions
FROM
    transactions
GROUP BY
    type;

-- Join transaction records with their type-level summary
SELECT
    t.step,
    t.type,
    t.amount,
    t.isFraud,
    s.transaction_count,
    s.fraudulent_transactions
FROM
    transactions AS t
    JOIN transaction_type_summary AS s ON t.type = s.type
LIMIT
    100;