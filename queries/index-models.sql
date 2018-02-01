-- indices will greatly slow down insertion. do this only after the table is populated.
CREATE INDEX IF NOT EXISTS raw_logs_model on raw_logs (model);
