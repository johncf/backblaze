help:
	@echo 'Usage:                                                                    '
	@echo '   make db-init        Create database, process and store data            '
	@echo '   make db-deindex     Remove all indices. Useful before loading more data'
	@echo '   make Results.md     Generate Results.md containing plots of 20 most    '
	@echo '                       popular disk models in database.                   '

db-init:
	./dbpopulate.sh

db-deindex:
ifeq ($(DROP), yes)
	psql backblaze -f queries/drop-index.sql
else
	@echo "You sure you want to drop all indices?"
	@echo "If so, use: make db-deindex DROP=yes"
endif

Results.md: plot-all plot-metadata
	./embed-plots.sh > Results.md

plot-all: plot-metadata failysis/basic-plot.py
	./plot-all.sh | bash
	touch plot-all

plot-metadata: popular-models
	./process-all.sh

popular-models:
	psql backblaze -f queries/index-models.sql
	psql backblaze -f queries/popular-models.sql | nl -nrz -w2 -s'|' - > popular-models

plot-scour: plot-all
	./scour-plots.sh | bash

plot-png: plot-all plot-metadata
	cut -f1 -d'|' plot-metadata | sed -e 's/^\(.*\)\.svg$$/inkscape -e \1.png \1.svg/' | bash

.PHONY: help db-init db-deindex plot-scour plot-png
