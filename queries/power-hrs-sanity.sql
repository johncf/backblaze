-- check for abrupt/unusual changes in power_hrs between consecutive logs.
-- a large positive change between consecutive logs might be due to a temporal gap between the logs during which the disk was active but not logged.
-- a negative change between consecutive logs might indicate that SMART counters were reset. This can cause inaccuracies in our calculations if there are too many of them.
SELECT *
FROM (SELECT datestamp,
             serial_no,
             power_hrs,
             lag(datestamp) OVER logging_per_serial AS prev_datestamp,
             power_hrs - lag(power_hrs) OVER logging_per_serial AS power_delta
      FROM disk_logs
      WINDOW logging_per_serial AS (PARTITION BY serial_no ORDER BY datestamp)
      LIMIT 20) AS laggy_logs
WHERE power_delta > 96 or power_delta < 0);
