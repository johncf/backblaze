CREATE TABLE IF NOT EXISTS raw_logs
(
    date DATE,        model TEXT,
    serial TEXT,      failed BOOLEAN,
    poh BIGINT,
    lba_r BIGINT,     lba_w BIGINT,
    PRIMARY KEY(date, serial)
);

---- indices will greatly slow down insertion
-- CREATE INDEX IF NOT EXISTS raw_logs_serial on raw_logs (serial);
-- CREATE INDEX IF NOT EXISTS raw_logs_poh on raw_logs (poh);
