#!/bin/bash

set -e -x

time psql backblaze -f index2.sql
time psql backblaze -f views.sql
time psql backblaze -f cumulative-failures.sql > fails.csv
time psql backblaze -f observed-population.sql > obs.csv
