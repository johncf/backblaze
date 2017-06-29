#!/bin/python2

import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter
import numpy as np
import math

import localdb

conn = localdb.connect()

outfile = "failure-rate-poh-3.svg"
param_name = "max_poh"
param_max_val = 25000
param_cumu_diff_tb = "poh_cumu_diff"
num_parts = 2000 # for interpolated sampling
window_size, poly_order = 69, 3 # for savgol filter

c = conn.cursor()
c.execute('''SELECT {0}, SUM(SUM(1)) OVER (ORDER BY {0})
             FROM devices
             WHERE fail_date IS NOT NULL AND
                   {0} IS NOT NULL AND
                   {0} < {1} AND
                   model='ST4000DM000'
             GROUP BY {0}'''.format(param_name, param_max_val))
fail_xs = []
fail_ys = []
for row in c:
  fail_xs.append(row[0])
  fail_ys.append(row[1])

c = conn.cursor()
c.execute('''SELECT val, SUM(n_diff) OVER (ORDER BY val) FROM {0}
             WHERE val < {1}'''.format(param_cumu_diff_tb, param_max_val))
obs_xs = []
obs_ys = []
for row in c:
  obs_xs.append(row[0])
  obs_ys.append(row[1])

conn.close()

# --- end data read to fail_*s and obs_*s ---

fx = np.array(fail_xs)
fy = np.array(fail_ys)

# interpolate
f_itp = interp1d(fx, fy, kind='linear')

fx_min = max(1., fx.min())
fx_max = fx.max()
x_f = np.linspace(fx_min, fx_max, num=num_parts)

# smooth
y_f_sg = savgol_filter(f_itp(x_f), window_size, poly_order)
dydx_f_sg = savgol_filter(f_itp(x_f), window_size, poly_order, deriv=1) / (fx_max - fx_min) * num_parts

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)

ax3.set_xlabel("Power-on hours")

ax1.set_ylabel("Cumulative failures")
ax1.set_ylim(0, 1500)

#ax1.scatter(fx[1:], fy[1:], c='g', marker='.')
ax1.plot(x_f, y_f_sg, 'b-')

ax12 = ax1.twinx()
ax12.set_ylabel("Derivative of cumulative failures")
ax12.set_yscale("log")
ax12.set_ylim(1e-4, 1)
ax12.plot(x_f, dydx_f_sg, 'r-')

ox = np.array(obs_xs)
oy = np.array(obs_ys)

o_itp = interp1d(ox, oy, kind='linear')
x_o = np.linspace(ox.min(), ox.max(), num=2000)

ax2.set_ylabel("Number of disks under observation")
ax2.set_yscale("log")
ax2.set_ylim(90, 1e5)
ax2.plot(x_o, o_itp(x_o))
#ax2.scatter(ox[1:], oy[1:], marker='.')

ax3.set_ylabel("Failure rate")
ax3.set_yscale("log")
ax3.set_ylim(1e-7, 1e-3)
y_fr = [y/o_itp(x) for (x, y) in zip(x_f, dydx_f_sg)]
ax3.plot(x_f, y_fr)

fig.set_size_inches(8, 12)
fig.savefig(outfile, bbox_inches="tight")
