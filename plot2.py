#!/bin/python2

import psycopg2 as pgs
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

def plot(ax, xs, ys, color='r', xlabels=[]):
  ax.scatter(xs, ys, s=5, marker=".", color=color)
  if len(xlabels) > 0:
    ax.xaxis.set_ticks(xs)
    ax.xaxis.set_ticklabels(xlabels)
  for tl in ax.get_yticklabels():
    tl.set_color(color)

conn = pgs.connect(database='backblaze2', user='john', password='john')

c = conn.cursor()
c.execute('''SELECT max_load_cc, max_poh FROM devices
             WHERE fail_date IS NOT NULL AND max_load_cc IS NOT NULL''')
fail_xs = []
fail_ys = []
for row in c:
  fail_xs.append(row[0])
  fail_ys.append(row[1])

fig, ax = plt.subplots()
ax.set_xlim([0.9, 1e7])
ax.set_xscale("log")
ax.set_xlabel("Load Cycles")
ax.set_ylim([0, 7e4])
ax.set_ylabel("Power-on Hours")
plot(ax, fail_xs, fail_ys)

plt.savefig("plot2.svg", bbox_inches="tight")
