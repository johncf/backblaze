#!/bin/bash
psql backblaze -f queries/popular-models.sql | nl -nrz -w2 -s'|' - > popular-models
