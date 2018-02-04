help:
	@echo 'Usage:                                                                    '
	@echo '   make db-init        Create database, process and store data            '
	@echo '   make db-deindex     Remove all indices. Do before loading more data.   '
	@echo '   make plot-all       Generate plots (dependency chain starts from       '
	@echo '                       querying for popular models in database)           '
	@echo '   make Results.md     Generate Results.md containing the plots           '

db-init:
	./dbpopulate.sh

db-deindex:
ifeq ($(DROP), yes)
	psql backblaze -f queries/drop-index.sql
else
	@echo "You sure you want to drop all indices?"
	@echo "If so, use: make db-deindex DROP=yes"
endif

Results.md: plot-metadata embed-plots.sh failysis/fail-stats.py
	./embed-plots.sh > Results.md

plot-all: plot-metadata failysis/basic-plot.py
	./plot-all.sh | bash

plot-metadata: popular-models
	./process-all.sh

popular-models:
	psql backblaze -f queries/index-models.sql
	psql backblaze -f queries/popular-models.sql | nl -nrz -w2 -s'|' - > popular-models

plot-scour:
	./scour-plots.sh | bash

plot-png: plot-metadata
	cut -f1 -d'|' plot-metadata | sed -e 's/^\(.*\)\.svg$$/inkscape -e \1.png \1.svg/' | bash

.PHONY: help db-init db-deindex plot-all plot-scour plot-png
