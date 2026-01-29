-- Postgres Performance Quick Check
-- Run this in your Supabase SQL Editor or psql to get a health snapshot.

\echo '--- 1. Cache Hit Ratios (Should be > 99%) ---'
SELECT 
  'index hit rate' as name,
  (sum(idx_blks_hit) - sum(idx_blks_read)) / sum(idx_blks_hit + idx_blks_read) as ratio 
FROM pg_statio_user_indexes
UNION ALL
SELECT 
  'table hit rate' as name, 
  sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) as ratio 
FROM pg_statio_user_tables;

\echo '\n--- 2. Unused Indexes (Wasted write performance) ---'
SELECT 
  schemaname || '.' || relname as table, 
  indexrelname as index, 
  idx_scan as num_scans,
  pg_size_pretty(pg_relation_size(indexrelid)) as size
FROM pg_stat_user_indexes 
JOIN pg_index USING (indexrelid)
WHERE idx_scan = 0 
  AND indisunique IS FALSE
ORDER BY pg_relation_size(indexrelid) DESC;

\echo '\n--- 3. Tables needing VACUUM (Dead tuples) ---'
SELECT 
  relname as table, 
  n_dead_tup as dead_tuples, 
  n_live_tup as live_tuples,
  ROUND((n_dead_tup::numeric / GREATEST(n_live_tup, 1)::numeric), 2) as ratio
FROM pg_stat_user_tables 
WHERE n_dead_tup > 1000 
ORDER BY n_dead_tup DESC;

\echo '\n--- 4. Active Long-Running Queries (> 1 min) ---'
SELECT 
  pid, 
  now() - query_start as duration, 
  state, 
  query 
FROM pg_stat_activity 
WHERE state != 'idle' 
  AND now() - query_start > interval '1 minute';
  
\echo '\n--- 5. Top 5 Slowest Queries (Requires pg_stat_statements) ---'
-- Uncomment if pg_stat_statements is enabled
-- SELECT 
--   substring(query, 1, 50) as query_snippet, 
--   calls, 
--   total_exec_time / calls as avg_time_ms 
-- FROM pg_stat_statements 
-- ORDER BY avg_time_ms DESC 
-- LIMIT 5;
