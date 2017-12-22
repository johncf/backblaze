CREATE TABLE IF NOT EXISTS raw_logs
( date DATE,        model TEXT,
  serial TEXT,      failed BOOLEAN,
  poh BIGINT,
  lba_r BIGINT,     lba_w BIGINT,
  PRIMARY KEY(date, serial)
);
