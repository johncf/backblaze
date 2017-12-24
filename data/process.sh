#!/bin/bash

set -e -x

time psql backblaze -f raw-index.sql
time psql backblaze -f raw-views.sql
time psql backblaze -f cumulative-failures.sql > fails.csv
time psql backblaze -f observed-population.sql > obs.csv
