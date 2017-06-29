CREATE TABLE load_cc_cumu_diff(val BIGINT PRIMARY KEY, n_diff INT);

INSERT INTO load_cc_cumu_diff (val, n_diff)
SELECT min_load_cc, SUM(1)
FROM devices
WHERE min_load_cc IS NOT NULL AND
      model='ST4000DM000'
GROUP BY min_load_cc;

INSERT INTO load_cc_cumu_diff (val, n_diff)
SELECT max_load_cc, SUM(-1)
FROM devices
WHERE max_load_cc IS NOT NULL AND
      model='ST4000DM000'
GROUP BY max_load_cc
ON CONFLICT (val)
DO UPDATE SET n_diff = load_cc_cumu_diff.n_diff + EXCLUDED.n_diff;

--------------------------------------------------------------------------------

CREATE TABLE poh_cumu_diff(val BIGINT PRIMARY KEY, n_diff INT);

INSERT INTO poh_cumu_diff (val, n_diff)
SELECT min_poh, SUM(1)
FROM devices
WHERE min_poh IS NOT NULL AND
      model='ST4000DM000'
GROUP BY min_poh;

INSERT INTO poh_cumu_diff (val, n_diff)
SELECT max_poh, SUM(-1)
FROM devices
WHERE max_poh IS NOT NULL AND
      model='ST4000DM000'
GROUP BY max_poh
ON CONFLICT (val)
DO UPDATE SET n_diff = poh_cumu_diff.n_diff + EXCLUDED.n_diff;

--------------------------------------------------------------------------------

CREATE TABLE io_cumu_diff(val BIGINT PRIMARY KEY, n_diff INT);

INSERT INTO io_cumu_diff (val, n_diff)
SELECT min_io, SUM(1)
FROM devices
WHERE min_io IS NOT NULL AND
      model='ST4000DM000'
GROUP BY min_io;

INSERT INTO io_cumu_diff (val, n_diff)
SELECT max_io, SUM(-1)
FROM devices
WHERE max_io IS NOT NULL AND
      model='ST4000DM000'
GROUP BY max_io
ON CONFLICT (val)
DO UPDATE SET n_diff = io_cumu_diff.n_diff + EXCLUDED.n_diff;

--------------------------------------------------------------------------------

SELECT val, sum(n_diff) OVER (ORDER BY val)
FROM load_cc_cumu_diff; -- ORDER BY val DESC;

SELECT max_load_cc, SUM(SUM(1)) OVER (ORDER BY max_load_cc)
FROM devices
WHERE fail_date IS NOT NULL AND
      max_load_cc IS NOT NULL
GROUP BY max_load_cc;
