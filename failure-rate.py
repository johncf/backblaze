#!/bin/python2

import psycopg2 as pgs
from plot2d import subplots, plot

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

# TODO

fig, ax = subplots()
# TODO
fig.savefig("failure-rate.svg", bbox_inches="tight")
