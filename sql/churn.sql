-- Churn = users who stop being active after signup

WITH user_activity AS (
    SELECT
        u.user_id,
        MIN(CAST(e.event_time AS DATE)) AS first_event,
        MAX(CAST(e.event_time AS DATE)) AS last_event
    FROM users u
    LEFT JOIN events e
        ON u.user_id = e.user_id
    GROUP BY u.user_id
),

churn_flag AS (
    SELECT
        user_id,
        CASE
            WHEN last_event < CURRENT_DATE - INTERVAL 14 DAY
            THEN 1
            ELSE 0
        END AS is_churned
    FROM user_activity
)

SELECT
    COUNT(*) AS total_users,
    SUM(is_churned) AS churned_users,
    ROUND(SUM(is_churned) * 100.0 / COUNT(*), 2) AS churn_rate
FROM churn_flag;
