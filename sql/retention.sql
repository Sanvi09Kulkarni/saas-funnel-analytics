WITH
signup AS (
    SELECT
        user_id,
        DATE_TRUNC('week', CAST(signup_date AS DATE)) AS cohort_date
    FROM users
),

events_clean AS (
    SELECT
        user_id,
        DATE_TRUNC('week', CAST(event_time AS DATE)) AS event_week
    FROM events
    WHERE event_type = 'feature_use'
),

user_weeks AS (
    SELECT
        s.user_id,
        s.cohort_date,
        e.event_week,
        FLOOR(DATEDIFF('day', s.cohort_date, e.event_week) / 7) AS week_number
    FROM signup s
    JOIN events_clean e USING(user_id)
),

cohort_sizes AS (
    SELECT
        cohort_date,
        COUNT(DISTINCT user_id) AS users_in_cohort
    FROM signup
    GROUP BY cohort_date
),

retention AS (
    SELECT
        cohort_date,
        week_number,
        COUNT(DISTINCT user_id) AS active_users
    FROM user_weeks
    WHERE week_number BETWEEN 0 AND 12
    GROUP BY cohort_date, week_number
)

SELECT
    r.cohort_date,
    r.week_number,
    ROUND(r.active_users * 100.0 / cs.users_in_cohort, 2) AS retention_percentage
FROM retention r
JOIN cohort_sizes cs USING(cohort_date)
ORDER BY cohort_date, week_number;
