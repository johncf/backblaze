#!/bin/bash

set -e -x

# create database 'backblaze' if not exists
psql -lqt | cut -d \| -f 1 | grep -qw backblaze || createdb backblaze

psql backblaze -f db.sql

for y in {2014..2017}; do
    FILTD=${y}_fil
    mkdir -p $FILTD
    for m in {01..12}; do
        pypy3 filter_csv.py $FILTD/${y}-${m}-xx.csv ${y}/${y}-${m}-*.csv
        ./dbcopy_csv.sh $FILTD/${y}-${m}-xx.csv
    done
done

set +x

echo "Done!"
echo "Edit prepare.sql to specify the disk model of interest, then run process.sh"
