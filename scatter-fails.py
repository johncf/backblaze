#!/bin/python2

import psycopg2 as pgs
from plot2d import subplots, plot
import sys

fname = sys.argv[1].strip()
if len(fname) == 0:
  sys.exit("No file name specified!")

conn = pgs.connect(database='backblaze2', user='john', password='john')

c = conn.cursor()

# models: 'ST%000DX000', 'ST4000DM000', 'ST3000DM001'
c.execute('''SELECT fail_lbarw, fail_poh FROM devices_io
             WHERE fail_lbarw IS NOT NULL AND model = 'ST4000DM000' ''')
#c.execute('''SELECT max_load_cc, max_poh FROM devices
#             WHERE fail_date IS NOT NULL AND max_load_cc IS NOT NULL AND model = 'ST4000DM000' ''')
fail_xs = []
fail_ys = []
for row in c:
  fail_ys.append(row[0])
  fail_xs.append(row[1])

fig, ax = subplots()
ax.set_yscale("log")

ax.set_xlabel("Power-on Hours")
plot(ax, fail_xs, fail_ys, "Blocks R/W", plttype="scatter") # "Load cycles"
ax.set_xlim(left=-5, right=30000)
#ax.set_ylim(bottom=0, top=4.2e11)
#ax.set_ylim(bottom=1e8, top=5e14)
#ax.set_ylim(bottom=0.9)
ax.set_ylim(bottom=1, top=1e12)

fig.set_size_inches(12, 6)
fig.savefig(fname, bbox_inches="tight", dpi=96)