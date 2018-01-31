DROP VIEW IF EXISTS disk_summary;
DROP VIEW IF EXISTS disk_logs;
DROP VIEW IF EXISTS disk_fails;

CREATE VIEW disk_logs AS
SELECT r.datestamp AS datestamp,
       r.serial AS serial_no,
       r.poh AS power_hrs,
       r.lba_r AS blocks_read,
       r.lba_w AS blocks_written
FROM raw_logs AS r
WHERE r.model = 'MMOODDEELL';

CREATE VIEW disk_fails AS
SELECT r.datestamp AS datestamp,
       r.serial AS serial_no
FROM raw_logs AS r
WHERE r.model = 'MMOODDEELL'
AND   r.failed;

CREATE VIEW disk_summary AS
SELECT serial_no,
       MIN(dl.datestamp) AS first_seen,
       MAX(dl.datestamp) AS last_seen,
       MIN(dl.power_hrs) AS min_power_hrs,
       MAX(dl.power_hrs) AS max_power_hrs
FROM disk_logs AS dl
GROUP BY serial_no;
