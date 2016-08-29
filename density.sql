CREATE TABLE lcc_poh_hist(
    lcc BIGINT,
    poh BIGINT,
    count INTEGER,
    PRIMARY KEY (lcc, poh)
);

-- useful max(lcc) is 2,000,000 and max(poh) is ~50,000
INSERT INTO lcc_poh_hist (lcc, poh, count)
SELECT load_cc/2000*2000, poh/50*50, sum(1)
FROM raw_logs
WHERE load_cc IS NOT NULL
GROUP BY load_cc/2000, raw_logs.poh/50;

CREATE TABLE io_poh_hist(
    io BIGINT,
    poh BIGINT,
    count INTEGER,
    PRIMARY KEY (io, poh)
);

-- max(lbarw) is ~1e14 (mostly ~1e11)
INSERT INTO io_poh_hist (io, poh, count)
SELECT (lba_r + lba_w)/500000000*500000000, poh/50*50, sum(1)
FROM raw_logs
WHERE lba_r IS NOT NULL
GROUP BY (lba_r + lba_w)/500000000, raw_logs.poh/50;

CREATE TABLE lcc_poh_hist_st4kdm(
    lcc BIGINT,
    poh BIGINT,
    count INTEGER,
    PRIMARY KEY (lcc, poh)
);

-- useful max(lcc) is 500,000 and max(poh) is ~30,000
INSERT INTO lcc_poh_hist_st4kdm (lcc, poh, count)
SELECT load_cc/500*500, poh/30*30, sum(1)
FROM raw_logs
WHERE load_cc IS NOT NULL AND model='ST4000DM000'
GROUP BY load_cc/500, raw_logs.poh/30;

CREATE TABLE io_poh_hist_st4kdm(
    io BIGINT,
    poh BIGINT,
    count INTEGER,
    PRIMARY KEY (io, poh)
);

-- max(lbarw) is ~1e11
INSERT INTO io_poh_hist_st4kdm (io, poh, count)
SELECT (lba_r + lba_w)/500000000*500000000, poh/30*30, sum(1)
FROM raw_logs
WHERE lba_r IS NOT NULL AND model='ST4000DM000'
GROUP BY (lba_r + lba_w)/500000000, raw_logs.poh/30;

CREATE TABLE lcc_poh_hist_st4kdm_log(
    lcc_log_166 INTEGER,
    poh INTEGER,
    count INTEGER,
    PRIMARY KEY (lcc_log_166, poh)
);

-- useful max(lcc) is 1,000,000 and max(poh) is ~30,000
INSERT INTO lcc_poh_hist_st4kdm_log (lcc_log_166, poh, count)
SELECT round(log(10, load_cc)*1000/6, 0), poh/30*30, sum(1)
FROM raw_logs
WHERE load_cc > 0 AND model='ST4000DM000'
GROUP BY round(log(10, load_cc)*1000/6, 0), raw_logs.poh/30;
