# Backblaze Data Analysis

A collection of scripts to prepare and process data published by Backblaze, to
generate failure rate curves over the age of a disk. The scripts needed for the
final generation of plots are kept in [failure-analysis repo][].

The steps described below assumes the presence of directories `2014`, `2015`,
`2016` and `2017` within [`data` directory][data], containing [Hard Drive Test
Data from Backblaze][backblaze] in csv format (i.e. after extracted them).

[failure-analysis repo]: https://gitlab.com/johncf/failure-analysis
[data]: ./data
[backblaze]: https://www.backblaze.com/b2/hard-drive-test-data.html

### Prepare Database: `dbpopulate.sh`

`dbpopulate.sh`, when executed, will create a Postgres database named
`backblaze` a table named `raw_logs` in it. It proceeds to populate it with
data from [`data` directory].

This uses `filter_csv.py` to create a csv file each for every month, which only
contains those fields necessary for the database. It then performs a [`COPY`][]
from the newly created csv file into the `raw_logs` table.

[`COPY`]: https://www.postgresql.org/docs/current/static/sql-copy.html

### Process Data: `process.sh`

`process.sh` crunches the data to produce two output files: `fails.csv` and
`obs.csv`. These files can be passed to `basic-plot.py` script from
[failure-analysis repo][failure-analysis] to generate annualized failure rate plot
against the age of the disk for the model of interest specified in `views.sql`.

Edit `views.sql` before running this if you want to specify another disk model
of interest. At the time of writing this, there was only one disk model with
enough data to generate a failure rate curve with low noise.

[failure-analysis]: https://gitlab.com/johncf/failure-analysis

### Results

TODO
