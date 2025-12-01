-- Estimate index bloat for user tables (approximate).
-- Run as a superuser or a role with access to all schemas.

WITH index_stats AS (
    SELECT
        schemaname,
        tablename,
        indexname,
        pg_relation_size(indexrelid) AS index_size_bytes,
        idx_scan,
        n_tup_ins,
        n_tup_upd,
        n_tup_del,
        n_live_tup,
        n_dead_tup
    FROM pg_stat_user_indexes
    JOIN pg_stat_user_tables USING (schemaname, tablename)
)
SELECT
    schemaname,
    tablename,
    indexname,
    pg_size_pretty(index_size_bytes) AS index_size,
    idx_scan,
    n_live_tup,
    n_dead_tup,
    ROUND(
        CASE
            WHEN n_live_tup = 0 THEN 0
            ELSE (n_dead_tup::numeric / GREATEST(n_live_tup, 1)) * 100
        END,
        2
    ) AS approx_dead_pct
FROM index_stats
ORDER BY approx_dead_pct DESC, index_size_bytes DESC
LIMIT 50;
