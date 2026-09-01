-- Transaction volume by type
SELECT
    type,
    COUNT(*) AS transaction_count,
    ROUND(SUM(amount), 2) AS total_amount,
    ROUND(AVG(amount), 2) AS average_amount
FROM
    transactions
GROUP BY
    type
ORDER BY
    transaction_count DESC;

-- Fraudulent transaction volume by type
SELECT
    type,
    COUNT(*) AS fraudulent_transactions,
    ROUND(SUM(amount), 2) AS fraudulent_amount,
    ROUND(AVG(amount), 2) AS average_fraud_amount
FROM
    transactions
WHERE
    isFraud = 1
GROUP BY
    type
ORDER BY
    fraudulent_transactions DESC;

-- Transaction types with more than 100,000 transactions
SELECT
    type,
    COUNT(*) AS transaction_count
FROM
    transactions
GROUP BY
    type
HAVING
    COUNT(*) > 100000
ORDER BY
    transaction_count DESC;

-- Time-step transaction activity
SELECT
    step,
    COUNT(*) AS transaction_count,
    SUM(isFraud) AS fraudulent_transactions,
    ROUND(AVG(amount), 2) AS average_amount
FROM
    transactions
GROUP BY
    step
ORDER BY
    step;