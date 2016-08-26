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
    PRIMARY KEY (lcc, poh)
);

-- max(lbarw) is ~1e14
INSERT INTO io_poh_hist (io, poh, count)
SELECT (lba_r + lba_w)/1e9*1e9, poh/50*50, sum(1)
FROM raw_logs
WHERE load_cc IS NOT NULL
GROUP BY (lba_r + lba_w)/1e9, raw_logs.poh/50;
