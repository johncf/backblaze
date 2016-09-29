#!/bin/python2

import matplotlib.pyplot as plt
import psycopg2 as pgs
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter
import numpy as np
import math

conn = pgs.connect(database='backblaze2', user='john', password='john')

outfile = "failure-rate-lcc-1.svg"
param_name = "max_load_cc"
param_max_val = 5900
param_cumu_diff_tb = "load_cc_cumu_diff"
num_parts = 2000

c = conn.cursor()
c.execute('''SELECT {0}, SUM(SUM(1)) OVER (ORDER BY {0})
             FROM devices
             WHERE fail_date IS NOT NULL AND {0} IS NOT NULL AND {0} < {1}
             GROUP BY {0}'''.format(param_name, param_max_val))
fail_xs = []
fail_ys = []
for row in c:
  fail_xs.append(row[0])
  fail_ys.append(row[1])

c = conn.cursor()
c.execute('''SELECT val, SUM(n_diff) OVER (ORDER BY val) FROM {0} WHERE val < {1}'''.format(param_cumu_diff_tb, param_max_val))
obs_xs = []
obs_ys = []
for row in c:
  obs_xs.append(row[0])
  obs_ys.append(row[1])

conn.close()

fx = np.array(fail_xs)
fy = np.array(fail_ys)

# interpolate
f_itp = interp1d(fx, fy, kind='linear')

fx_max = fx.max()
x_f = np.linspace(1., fx_max, num=num_parts)

# smooth
window_size, poly_order = 39, 4
y_f_sg = savgol_filter(f_itp(x_f), window_size, poly_order)
dydx_f_sg = savgol_filter(f_itp(x_f), window_size, poly_order, deriv=1) / (fx_max / num_parts)

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)

ax3.set_xlabel("Load cycles")

#ax1.set_xscale("log")
ax1.set_ylabel("Cumulative failures")
ax1.set_ylim(0, 3500)

#ax1.scatter(fx[1:], fy[1:], c='b', marker='x')
ax1.plot(x_f, y_f_sg, 'g-')

ax12 = ax1.twinx()
ax12.set_ylabel("Derivative of cumulative failures")
ax12.set_yscale("log")
ax12.set_ylim(1e-6, 16)
ax12.plot(x_f, dydx_f_sg, 'r-')

ox = np.array(obs_xs)
oy = np.array(obs_ys)

o_itp = interp1d(ox, oy, kind='linear')
x_o = np.linspace(1., ox.max(), num=2000)

ax2.set_ylabel("Number of disks under observation")
#ax2.set_xscale("log")
ax2.set_yscale("log")
ax2.set_ylim(10, 1e5)
ax2.plot(x_o, o_itp(x_o))
#ax2.scatter(ox[1:], oy[1:], marker='.')

ax3.set_ylabel("Failure rate")
ax3.set_yscale("log")
ax3.set_ylim(1e-8, 1)
y_fr = [y/o_itp(x) for (x, y) in zip(x_f, dydx_f_sg)]
ax3.plot(x_f, y_fr)

fig.set_size_inches(8, 12)
fig.savefig(outfile, bbox_inches="tight")
