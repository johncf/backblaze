-- indices will greatly slow down insertion. do this only after the table is populated.
CREATE INDEX IF NOT EXISTS raw_logs_serial on raw_logs (serial);
CREATE INDEX IF NOT EXISTS raw_logs_failed on raw_logs (failed);
CREATE INDEX IF NOT EXISTS raw_logs_model on raw_logs (model);
CREATE INDEX IF NOT EXISTS raw_logs_model_serial on raw_logs (model, serial);

SELECT model, COUNT(serial) AS fail_count FROM raw_logs WHERE failed GROUP BY model ORDER BY fail_count DESC LIMIT 10;
