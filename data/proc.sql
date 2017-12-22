-- indices will greatly slow down insertion. do this only after the table is populated.
CREATE INDEX IF NOT EXISTS raw_logs_serial on raw_logs (serial);
CREATE INDEX IF NOT EXISTS raw_logs_failed on raw_logs (failed);

CREATE VIEW disk_logs AS
SELECT r.date AS datestamp,
       r.serial AS serial_no,
       r.poh AS power_hrs,
       r.lba_r AS blocks_read,
       r.lba_w AS blocks_written
FROM raw_logs AS r;

CREATE VIEW disk_fails AS
SELECT r.date AS datestamp,
       r.serial AS serial_no
FROM raw_logs AS r
WHERE failed;
