#!/bin/python2

import matplotlib.pyplot as plt
import psycopg2 as pgs
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter
import numpy as np
import math

conn = pgs.connect(database='backblaze', user='john', password='john')

c = conn.cursor()
c.execute('''SELECT max_load_cc, SUM(SUM(1)) OVER (ORDER BY max_load_cc)
             FROM devices
             WHERE fail_date IS NOT NULL AND max_load_cc IS NOT NULL
             GROUP BY max_load_cc''')
fail_xs = []
fail_ys = []
for row in c:
  fail_xs.append(row[0])
  fail_ys.append(row[1])

c = conn.cursor()
c.execute('''SELECT val, SUM(n_diff) OVER (ORDER BY val) FROM load_cc_cumu_diff''')
obs_xs = []
obs_ys = []
for row in c:
  obs_xs.append(row[0])
  obs_ys.append(row[1])

conn.close()

fx = np.array(fail_xs[:-12])
fy = np.array(fail_ys[:-12])

# interpolate
f_itp = interp1d(fx, fy, kind='linear')

#x_f = np.logspace(0., math.log(fx.max(), 10), num=1000)
x_f = np.linspace(1., fx.max(), num=2000)

# smooth
window_size, poly_order = 39, 4
y_f_sg = savgol_filter(f_itp(x_f), window_size, poly_order)
dydx_f_sg = savgol_filter(f_itp(x_f), window_size, poly_order, deriv=1)

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)

ax3.set_xlabel("Load cycles")

#ax1.set_xscale("log")
ax1.set_ylabel("Cumulative failures")

#ax1.scatter(fx[1:100], fy[1:100], c='b', marker='x')
#ax1.scatter(x_f, f_itp(x_f), c='r', marker='o')
ax1.plot(x_f, y_f_sg, 'g-')

ax12 = ax1.twinx()
ax12.set_ylabel("Derivative of cumulative failures")
ax12.set_yscale("log")
#ax12.set_ylim(-1, 20)
ax12.plot(x_f, dydx_f_sg, 'r-')

ox = np.array(obs_xs[:-200])
oy = np.array(obs_ys[:-200])

o_itp = interp1d(ox, oy, kind='linear')
x_o = np.linspace(1., ox.max(), num=2000)

ax2.set_ylabel("Number of disks under observation")
#ax2.set_xscale("log")
ax2.set_yscale("log")
ax2.plot(x_o, o_itp(x_o))
#ax2.scatter(ox[1:], oy[1:], marker='.')

ax3.set_ylabel("Failure rate")
ax3.set_yscale("log")
y_fr = [y/o_itp(x) for (x, y) in zip(x_f, dydx_f_sg)]
ax3.plot(x_f, y_fr)

fig.set_size_inches(8, 12)
fig.savefig("failure-rate.svg", bbox_inches="tight")
