# Prepare Database

Download the data from [their official page][backblaze], and extract it to
directories corresponding to each year.

[backblaze]: https://www.backblaze.com/b2/hard-drive-test-data.html

### `dbpopulate.sh`

This is the main script that when executed will create a postgres database
named `backblaze`, create a table named `raw_logs` with structure defined in
`db.sql` and populate it with data from Backblaze. This script assumes that the
current directory contains directories named `2014`, `2015`, `2016` and `2017`
which contains the csv data files from Backblaze.

This uses `filter_csv.py` to create a csv file each for every month, which only
contains what is needed for the database. It then calls `dbcopy_csv.sh` with
that filtered csv file to do a `COPY` operation into the `raw_logs` table.

Edit the script as needed. I used `pypy3` for faster execution of
`filter_csv.py`. Change it to `python3` if you see fit.

### `smart_csv2json.py`

This is a convenience script to view a Backblaze csv file as a json list of
objects, where the object key is human-friendly in that it contains a
meaningful name for each SMART value. Example invocation:

    $ cat 2015/2015-01-01.csv | ./smart_csv2json.py | head -n 44
