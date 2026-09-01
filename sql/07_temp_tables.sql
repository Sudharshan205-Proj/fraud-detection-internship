DROP TABLE IF EXISTS fraud_summary;

CREATE TEMP
TABLE fraud_summary AS
SELECT
    type,
    COUNT(*) AS total_transactions,
    SUM(isFraud) AS fraudulent_transactions,
    AVG(amount) AS average_amount
FROM
    transactions
GROUP BY
    type;

SELECT
    type,
    total_transactions,
    fraudulent_transactions,
    ROUND(average_amount, 2) AS average_amount
FROM
    fraud_summary
ORDER BY
    fraudulent_transactions DESC;