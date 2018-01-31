#!/bin/bash
set -e
echo > metadata
tail -n+2 popular-models | tr -s ' ' | cut -f1-2 -d'|' | while read line
do
    IFS='|' read -r -a array <<< "$line"
    id=${array[0]%% }
    model=${array[1]## }
    model=${model%% }
    if wc -l $id-fails.csv 2>\dev\null && wc -l $id-obs.csv 2>\dev\null; then
        echo "Skipping $model"
    else
        echo "Processing ${model}"
        psql backblaze -f <(sed "s/MMOODDEELL/${model}/g" queries/views.sql)
        psql backblaze -f queries/cumulative-failures.sql > $id-fails.csv || {
            rm $id-fails.csv && false
        }
        wc -l $id-fails.csv
        psql backblaze -f queries/observed-population.sql > $id-obs.csv || {
            rm $id-obs.csv && false
        }
        wc -l $id-obs.csv
    fi
    echo "$id-plot.svg|$id-fails.csv|$id-obs.csv|$model" >> metadata
done
