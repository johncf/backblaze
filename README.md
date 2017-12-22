# Backblaze Data Analysis

A bunch of scripts to import backblaze data into Postgres database, and analyze
data using that database.

See README in [data directory][] for how to prepare the database from raw
Backblaze data.

After this is done, refer to the SQL queries inside [queries directory][] to
preprocess the data to make it ready for consumption by other scripts.

All other python scripts in the directory is used to generate various types of
plots from the data.

To see the generated plots, see [backblaze-plots][].

[pgdb]: localdb.py#L4
[backblaze-plots]: https://gitlab.com/johncf/backblaze-plots
[data directory]: data
[queries directory]: queries
