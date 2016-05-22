CREATE TABLE IF NOT EXISTS devices
(
    serial TEXT PRIMARY KEY,
    model TEXT,
    min_date DATE,
    max_date DATE,
    min_load_cc BIGINT,
    max_load_cc BIGINT,
    fail_date DATE
);

INSERT INTO devices (serial, model, min_date, max_date, min_load_cc, max_load_cc)
SELECT serial, MIN(model), MIN(date), MAX(date), MIN(load_cc), MAX(load_cc)
FROM raw_logs GROUP BY serial;

-- update fail_date
UPDATE devices
SET fail_date = failures.date
FROM (SELECT serial, date FROM raw_logs WHERE failed) AS failures
WHERE devices.serial = failures.serial;

-- inconsistencies

CREATE TABLE IF NOT EXISTS devices_blacklist
(
    serial TEXT PRIMARY KEY,
    model TEXT -- FYI
);

INSERT INTO devices_blacklist (serial, model)
SELECT devices.serial, devices.model -- see: max_load_cc, load_cc, max_date
FROM devices, raw_logs
WHERE (raw_logs.serial = devices.serial AND date = max_date) AND
      max_load_cc != load_cc
ON CONFLICT DO NOTHING;

INSERT INTO devices_blacklist (serial, model)
SELECT devices.serial, devices.model -- see: min_load_cc, load_cc, min_date
FROM devices, raw_logs
WHERE (raw_logs.serial = devices.serial AND date = min_date) AND
      min_load_cc != load_cc
ON CONFLICT DO NOTHING;

DELETE FROM raw_logs WHERE serial IN (SELECT serial FROM devices_blacklist);
DELETE FROM devices WHERE serial IN (SELECT serial FROM devices_blacklist);

SELECT model, COUNT(*)
FROM devices
WHERE fail_date != max_date
GROUP BY model;

-- logs after device failure but not showing any further IO activity
DELETE FROM raw_logs
USING (SELECT devices.serial, date
       FROM raw_logs, devices
       WHERE raw_logs.serial = devices.serial AND
             date = fail_date + INTERVAL '1' DAY AND
             load_cc = devices.max_load_cc
      ) dead_logs
WHERE raw_logs.serial = dead_logs.serial AND
      raw_logs.date >= dead_logs.date;

-- *or* just delete all logs after the first failure
--DELETE FROM raw_logs
--USING (SELECT devices.serial, fail_date
--       FROM raw_logs, devices
--       WHERE raw_logs.serial = devices.serial AND
--             fail_date IS NOT NULL) post_fail_logs
--WHERE raw_logs.serial = post_fail_logs.serial AND
--      raw_logs.date > post_fail_logs.fail_date;

-- update max_date
UPDATE devices
SET max_date = failed_devs.max_date
FROM (SELECT raw_logs.serial, MAX(date) as max_date
      FROM raw_logs, devices
      WHERE raw_logs.serial = devices.serial AND
            fail_date IS NOT NULL
      GROUP BY raw_logs.serial
     ) AS failed_devs
WHERE devices.serial = failed_devs.serial;

SELECT serial, COUNT(failed)
FROM raw_logs
WHERE failed
GROUP BY serial
HAVING COUNT(failed) > 1;
