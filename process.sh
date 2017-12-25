#!/bin/bash

set -e -x

time psql backblaze -f queries/index2.sql
time psql backblaze -f queries/views.sql
time psql backblaze -f queries/cumulative-failures.sql > fails.csv
time psql backblaze -f queries/observed-population.sql > obs.csv
