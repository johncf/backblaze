#!/bin/bash

set -e -x

# create database 'backblaze' if not exists
psql -lqt | cut -d \| -f 1 | grep -qw backblaze || createdb backblaze

psql backblaze -f queries/base.sql

for y in {2013..2017}; do
    FILTD=data/${y}_fil
    mkdir -p $FILTD
    for m in {01..12}; do
        if ls data/${y}/${y}-${m}-*.csv 1>/dev/null 2>&1; then
            # NOTE: Use `pypy3` below for faster execution.
            ./filter_csv.py $FILTD/${y}-${m}-xx.csv data/${y}/${y}-${m}-*.csv
            psql backblaze -f queries/copy-raw.sql < $FILTD/${y}-${m}-xx.csv
        fi
    done
done

psql backblaze -f queries/index1.sql

set +x

echo "Done!"
echo "Run get-popular-models.sh script to generate popular-models table."
echo "Then run process-all.sh"
