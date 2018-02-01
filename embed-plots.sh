#!/bin/bash
set -e
cat plot-metadata | while read line
do
    IFS='|' read -r -a array <<< "$line"
    model=${array[3]}
    plot=${array[0]}
    fails=${array[1]}
    obsct=${array[2]}

    statsstr=$(./failysis/fail-stats.py -m $fails $obsct)
    IFS=' ' read -r -a stats <<< "$statsstr"

    echo "### $model"
    echo
    echo "**Total disk-years observed:** ${stats[0]} <br>"
    echo "**Total failures observed:** ${stats[1]} <br>"
    echo "**Mean AFR over lifetime:** ${stats[2]}"
    echo
    echo "![]($plot)"
    echo
done
