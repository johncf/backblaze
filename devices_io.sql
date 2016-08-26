CREATE TABLE IF NOT EXISTS devices_io
(
    serial TEXT PRIMARY KEY,
    model TEXT,
    min_date DATE,
    max_date DATE,
    min_lbarw BIGINT,
    max_lbarw BIGINT,
    min_poh BIGINT,
    max_poh BIGINT,
    fail_date DATE,
    fail_lbarw BIGINT,
    fail_poh BIGINT
);

INSERT INTO devices_io (serial, model, min_date, max_date, min_lbarw, max_lbarw, min_poh, max_poh)
SELECT serial, MIN(model), MIN(date), MAX(date), MIN(lba_r+lba_w), MAX(lba_r+lba_w), MIN(poh), MAX(poh)
FROM raw_logs GROUP BY serial;

-- update fail_date
UPDATE devices_io
SET fail_date = failures.date, fail_lbarw = failures.lba_rw, fail_poh = failures.poh
FROM (SELECT serial, date, lba_r + lba_w AS lba_rw, poh FROM raw_logs WHERE failed) AS failures
WHERE devices_io.serial = failures.serial;

-- sanitize inconsistencies

CREATE TABLE IF NOT EXISTS blacklist_io
(
    serial TEXT PRIMARY KEY,
    model TEXT, -- FYI
    reason TEXT
);

-- max_lbarw not at fail_date
INSERT INTO blacklist_io (serial, model, reason)
SELECT devices_io.serial, devices_io.model, 'zombie_usage'
FROM devices_io, raw_logs
WHERE (raw_logs.serial = devices_io.serial AND date = fail_date) AND
      max_lbarw != lba_r+lba_w
ON CONFLICT DO NOTHING;

-- max_lbarw not at max_date
INSERT INTO blacklist_io (serial, model, reason)
SELECT devices_io.serial, devices_io.model, 'max_mismatch'
FROM devices_io, raw_logs
WHERE (raw_logs.serial = devices_io.serial AND date = max_date) AND
      max_lbarw != lba_r+lba_w
ON CONFLICT DO NOTHING;

-- min_lbarw not at min_date
INSERT INTO blacklist_io (serial, model, reason)
SELECT devices_io.serial, devices_io.model, 'min_mismatch'
FROM devices_io, raw_logs
WHERE (raw_logs.serial = devices_io.serial AND date = min_date) AND
      min_lbarw != lba_r+lba_w
ON CONFLICT DO NOTHING;

DELETE FROM devices_io WHERE serial IN (SELECT serial FROM blacklist_io);

SELECT model, COUNT(*)
FROM devices_io
WHERE fail_date != max_date
GROUP BY model;

-- logs after device failure but not showing any further IO activity
DELETE FROM raw_logs
USING (SELECT devices_io.serial, date
       FROM raw_logs, devices_io
       WHERE raw_logs.serial = devices_io.serial AND
             date = fail_date + INTERVAL '1' DAY AND
             lba_r+lba_w = devices_io.max_lbarw
      ) dead_logs
WHERE raw_logs.serial = dead_logs.serial AND
      raw_logs.date >= dead_logs.date;

-- *or* just delete all logs after the first failure
--DELETE FROM raw_logs
--USING (SELECT devices_io.serial, fail_date
--       FROM raw_logs, devices_io
--       WHERE raw_logs.serial = devices_io.serial AND
--             fail_date IS NOT NULL) post_fail_logs
--WHERE raw_logs.serial = post_fail_logs.serial AND
--      raw_logs.date > post_fail_logs.fail_date;

-- update max_date
UPDATE devices_io
SET max_date = failed_devs.max_date
FROM (SELECT raw_logs.serial, MAX(date) as max_date
      FROM raw_logs, devices_io
      WHERE raw_logs.serial = devices_io.serial AND
            fail_date IS NOT NULL
      GROUP BY raw_logs.serial
     ) AS failed_devs
WHERE devices_io.serial = failed_devs.serial;

SELECT serial, COUNT(failed)
FROM raw_logs
WHERE failed
GROUP BY serial
HAVING COUNT(failed) > 1;
