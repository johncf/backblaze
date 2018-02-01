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

plot-all: plot-metadata
	./plot-all.sh | bash
	touch plot-all

plot-metadata: popular-models
	./process-all.sh

popular-models:
	psql backblaze -f queries/index-models.sql
	psql backblaze -f queries/popular-models.sql | nl -nrz -w2 -s'|' - > popular-models

minify-plots: plot-all
	./scour-plots.sh | bash

.PHONY: help db-init db-deindex minify-plots
