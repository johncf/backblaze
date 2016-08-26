#!/bin/python2

#from mpl_toolkits.mplot3d import proj3d
from matplotlib import cm
import psycopg2 as pgs
import matplotlib.pyplot as plt
import numpy as np
import math

zv = np.zeros((1000, 1000))

conn = pgs.connect(database='backblaze2', user='john', password='john')
cur = conn.cursor()
cur.execute('''SELECT poh, lcc, count FROM lcc_poh_hist''')

for row in cur:
  poh_i = row[0]/50
  lcc_i = row[1]/2000
  if lcc_i > 0 and poh_i < 1000 and lcc_i < 1000:
    zv[lcc_i, poh_i] = math.log10(row[2])

plt.clf()
plt.imshow(zv, origin='lower', extent=(0, 50e3, 0, 2e6), aspect=2.0/100)

plt.savefig("lcc-poh-heat.svg", bbox_inches="tight", dpi=96)
