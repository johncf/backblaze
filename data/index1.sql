-- indices will greatly slow down insertion. do this only after the table is populated.
CREATE INDEX IF NOT EXISTS raw_logs_failed on raw_logs (failed);

SELECT model, COUNT(serial) AS fail_count FROM raw_logs WHERE failed GROUP BY model ORDER BY fail_count DESC LIMIT 10;
