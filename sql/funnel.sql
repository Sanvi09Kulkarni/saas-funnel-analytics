WITH signup AS (
    SELECT
        user_id,
        CAST(signup_date AS DATE) AS signup_date
    FROM users
),

activation AS (
    SELECT
        u.user_id,
        MIN(CAST(e.event_time AS DATE)) AS activation_date,
        COUNT(*) FILTER (WHERE e.event_type = 'feature_use') AS feature_count
    FROM signup u
    JOIN events e ON u.user_id = e.user_id
    WHERE CAST(e.event_time AS DATE)
        BETWEEN u.signup_date
        AND u.signup_date + INTERVAL '30 days'
    GROUP BY u.user_id
    HAVING feature_count >= 3
),

paid AS (
    SELECT
        user_id,
        CAST(start_date AS DATE) AS subscription_date
    FROM subscriptions
),

paid_after_activation AS (
    SELECT
        p.user_id,
        p.subscription_date
    FROM paid p
    JOIN activation a ON p.user_id = a.user_id
    WHERE p.subscription_date > a.activation_date
)

SELECT
    (SELECT COUNT(*) FROM signup) AS total_users,
    (SELECT COUNT(*) FROM activation) AS activated_users,
    (SELECT COUNT(*) FROM paid_after_activation) AS paid_users,
    ROUND((SELECT COUNT(*) FROM activation) * 100.0
        / (SELECT COUNT(*) FROM signup), 2) AS activation_rate,
    ROUND((SELECT COUNT(*) FROM paid_after_activation) * 100.0
        / (SELECT COUNT(*) FROM signup), 2) AS paid_conversion_rate,
    ROUND((SELECT COUNT(*) FROM paid_after_activation) * 100.0
        / (SELECT COUNT(*) FROM activation), 2) AS post_activation_conversion_rate;
