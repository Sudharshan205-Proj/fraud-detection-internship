-- Transactions whose amount is greater than
-- the overall average transaction amount
SELECT
    step,
    type,
    amount,
    isFraud
FROM
    transactions
WHERE
    amount > (
        SELECT
            AVG(amount)
        FROM
            transactions
    )
ORDER BY
    amount DESC
LIMIT
    100;

-- Fraud types whose fraud rate is above the
-- overall fraud rate
SELECT
    type,
    COUNT(*) AS total_transactions,
    SUM(isFraud) AS fraudulent_transactions,
    100.0 * SUM(isFraud) / COUNT(*) AS fraud_rate
FROM
    transactions
GROUP BY
    type
HAVING
    (1.0 * SUM(isFraud) / COUNT(*)) > (
        SELECT
            1.0 * SUM(isFraud) / COUNT(*)
        FROM
            transactions
    );