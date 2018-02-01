#!/bin/bash
echo 'set -e'
cat plot-metadata | awk -F'|' '{print "failysis/basic-plot.py -x -o", $1, "-T \"Model: " $4 "\"", $2, $3}'
