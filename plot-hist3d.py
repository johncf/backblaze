#!/bin/python2

import matplotlib.pyplot as plt
import numpy as np
import math
from mpl_toolkits.mplot3d import proj3d
from matplotlib import cm

import localdb

table = 'lcc_poh_hist'
var2 = 'lcc'
var2_factor = 2000
#table = 'io_poh_hist'
#var2 = 'io'
#var2_factor = int(5e8)

fig = plt.figure()
ax = fig.gca(projection='3d')

xs = np.arange(0, 50000, 50)
ys = np.arange(0, 1000*var2_factor, var2_factor)

xv, yv = np.meshgrid(xs, ys)
zv = np.zeros((1000, 1000))

conn = localdb.connect()

cur = conn.cursor()
cur.execute('''SELECT poh, {0}, count FROM {1}'''.format(var2, table))

for row in cur:
  xi = row[0]/50
  yi = row[1]/var2_factor
  if xi < 1000 and yi < 1000:
    zv[yi, xi] = math.log10(row[2])

ax.view_init(azim=40) #130
surf = ax.plot_surface(xv, yv, zv, rstride=10, cstride=10, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

fig.set_size_inches(16, 12)
fig.savefig("{0}-poh-hist.svg".format(var2), bbox_inches="tight", dpi=96)
