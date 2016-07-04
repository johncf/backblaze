#!/bin/python2

import psycopg2 as pgs
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

def plot(ax, xs, ys, ylabel, plttype="plot", color='r', xlabels=[]):
  if plttype == "scatter":
    ax.scatter(xs, ys, marker="x", color=color)
  else:
    ax.plot(xs, ys, color=color)
  if len(xlabels) > 0:
    ax.xaxis.set_ticks(xs)
    ax.xaxis.set_ticklabels(xlabels)
  ax.set_ylabel(ylabel)
  for tl in ax.get_yticklabels():
    tl.set_color(color)

def plot_twin(ax, xs, ys, ylabel, plttype="plot", color='b'):
  ax2 = ax.twinx()
  plot(ax2, xs, ys, ylabel, plttype, color)

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
pop_xs = []
pop_ys = []
for row in c:
  pop_xs.append(row[0])
  pop_ys.append(row[1])

fig, ax = plt.subplots()
ax.set_xscale("log")
ax.set_xlabel("Number of load cycles")
plot(ax, fail_xs, fail_ys, "Cumulative number of failures")
plot_twin(ax, pop_xs, pop_ys, "Number of disks under observation")

plt.savefig("plot.svg", bbox_inches="tight")
