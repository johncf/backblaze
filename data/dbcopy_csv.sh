#!/bin/bash

[ -z "$1" ] && {
    echo "Usage: $0 table.csv" >&2
    exit
}

exec psql -d backblaze -c "COPY raw_logs (date, model, serial, failed, poh, lba_r, lba_w) FROM STDIN WITH DELIMITER AS ',' NULL AS ''" < $1
