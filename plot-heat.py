#!/bin/python2

from matplotlib import cm
import psycopg2 as pgs
import matplotlib.pyplot as plt
import numpy as np
import math

table = 'lcc_poh_hist_st4kdm'
var2 = 'lcc'
var2_factor = 500

#table = 'io_poh_hist_st4kdm'
#var2 = 'io'
#var2_factor = int(5e8)

poh_factor = 30

#table = 'lcc_poh_hist_st4kdm_log'
#var2 = 'lcc'
#var2_factor = 1
var2_log_factor = 1 #6.0/1000

zv = np.zeros((1000, 1000))

conn = pgs.connect(database='backblaze2', user='john', password='john')
cur = conn.cursor()
cur.execute('''SELECT poh, {0}, count FROM {1}'''.format(var2, table))

for row in cur:
  poh_i = row[0]/poh_factor
  var2_i = row[1]/var2_factor
  if poh_i < 1000 and var2_i < 1000: # and var2_i > 0:
    zv[var2_i, poh_i] = math.log10(row[2])

fig, ax = plt.subplots(figsize=(12, 6))
ax.imshow(zv, origin='lower', extent=(0, poh_factor*1e3, 0, var2_factor*var2_log_factor*1e3), aspect=1.0/2*poh_factor/var2_factor/var2_log_factor)

fig.savefig("{0}-plots/heat-st4kdm-2.svg".format(var2), bbox_inches="tight", dpi=96)
