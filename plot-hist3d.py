#!/bin/python2

from mpl_toolkits.mplot3d import proj3d
from matplotlib import cm
import psycopg2 as pgs
import matplotlib.pyplot as plt
import numpy as np
import math

fig = plt.figure()
ax = fig.gca(projection='3d')

xs = np.arange(0, 50000, 50)
ys = np.arange(0, 2000000, 2000)

xv, yv = np.meshgrid(xs, ys)
zv = np.zeros((1000, 1000))

conn = pgs.connect(database='backblaze2', user='john', password='john')

c = conn.cursor()

c.execute('''SELECT poh, lcc, count FROM lcc_poh_hist''')

for row in c:
  xi = row[0]/50
  yi = row[1]/2000
  if xi < 1000 and yi < 1000:
    zv[xi, yi] = math.log10(row[2])

ax.view_init(azim=40) #310
surf = ax.plot_surface(xv, yv, zv, rstride=10, cstride=10, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

fig.set_size_inches(16, 12)
fig.savefig("lcc-poh-hist.svg", bbox_inches="tight", dpi=96)
