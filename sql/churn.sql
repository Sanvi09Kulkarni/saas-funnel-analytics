WITH last_activity AS (
    SELECT
        user_id,
        MAX(CAST(event_time AS TIMESTAMP)) AS last_active_at
    FROM events
    WHERE event_type = 'feature_use'
    GROUP BY user_id
),

dataset_max_date AS (
    SELECT
        MAX(CAST(event_time AS TIMESTAMP)) AS max_event_time
    FROM events
),

churned_users AS (
    SELECT
        u.user_id
    FROM users u
    LEFT JOIN last_activity l
        ON u.user_id = l.user_id
    CROSS JOIN dataset_max_date d
    WHERE l.last_active_at < d.max_event_time - INTERVAL 30 DAY
       OR l.last_active_at IS NULL
)

SELECT
    (SELECT COUNT(*) FROM users) AS total_users,
    (SELECT COUNT(*) FROM churned_users) AS churned_users,
    ROUND(
        (SELECT COUNT(*) FROM churned_users) * 100.0 /
        NULLIF((SELECT COUNT(*) FROM users), 0),
        2
    ) AS churn_rate;
