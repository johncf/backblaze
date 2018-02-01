#!/bin/bash
set -e

PROCDIR=processed
PLOTDIR=plots
mkdir -p $PROCDIR $PLOTDIR

truncate -s0 plot-metadata
cat popular-models | cut -f1-2 -d'|' | while read line
do
    IFS='|' read -r -a array <<< "$line"
    id=${array[0]}
    model=${array[1]}
    PLOTF=$PLOTDIR/$id-plot.svg
    FAILS=$PROCDIR/$id-fails.csv
    OBSCT=$PROCDIR/$id-obsct.csv
    if wc -l $FAILS 2>/dev/null && wc -l $OBSCT 2>/dev/null; then
        echo "Skipping $model"
    else
        echo "Processing ${model}"
        psql backblaze -f <(sed "s/MMOODDEELL/${model}/g" queries/views.sql)
        psql backblaze -f queries/cumulative-failures.sql > $FAILS || {
            rm $FAILS && false
        }
        wc -l $FAILS
        psql backblaze -f queries/observed-population.sql > $OBSCT || {
            rm $OBSCT && false
        }
        wc -l $OBSCT
    fi
    echo "$PLOTF|$FAILS|$OBSCT|$model" >> plot-metadata
done
