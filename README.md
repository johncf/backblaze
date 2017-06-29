# Backblaze Data Analysis

A bunch of scripts to import backblaze data into Postgres database, and analyze
data using that database.

First, you need to download the data from here [their official page][backblaze].
Then, provide the database credentials in [`localdb.py`][pgdb] and run the
script as follows:

    ./import_csv.py /path/to/data/*.csv

This will import all csv files from that data directory into the database.

After this is done, refer to the SQL queries inside [queries][] directory to
preprocess the data to make it ready for consumption by other scripts.

All other python scripts in the directory is used to generate various types of
plots from the data.

To see the generated plots, see [backblaze-plots][].

[backblaze]: https://www.backblaze.com/b2/hard-drive-test-data.html
[pgdb]: localdb.py#L4
[queries]: queries
[backblaze-plots]: https://gitlab.com/johncf/backblaze-plots
