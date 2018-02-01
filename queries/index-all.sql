-- to see stats about index usage, do `SELECT * FROM pg_stat_user_indexes;`
-- to reset those stats, do `SELECT pg_stat_reset();`
CREATE INDEX IF NOT EXISTS raw_logs_failed on raw_logs (failed);
CREATE INDEX IF NOT EXISTS raw_logs_model on raw_logs (model);
CREATE INDEX IF NOT EXISTS raw_logs_serial on raw_logs (serial);
CREATE INDEX IF NOT EXISTS raw_logs_model_serial on raw_logs (model, serial);
