#!/bin/python3

import psycopg2 as pgs
import csv
import os

def init(conn):
  c = conn.cursor()
  c.execute('''CREATE TABLE IF NOT EXISTS raw_logs
               (
                   date DATE,        model TEXT,
                   serial TEXT,      failed BOOLEAN,
                   poh BIGINT,       lba_w BIGINT,
                   lba_r BIGINT,     load_cc BIGINT,
                   PRIMARY KEY(date, serial)
               )''')
  c.execute('''CREATE INDEX IF NOT EXISTS raw_logs_serial on raw_logs (serial)''')
  c.execute('''CREATE INDEX IF NOT EXISTS raw_logs_poh on raw_logs (poh)''')
  conn.commit()

def clean(s):
  s = s.strip()
  if not s:
    return None
  else:
    return s

def csv_import(conn, csvfile):
  c = conn.cursor()
  insert_query = '''INSERT INTO raw_logs (date, model, serial, failed,
                                          poh,  lba_w, lba_r,  load_cc)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING'''
  total = 0
  affected = 0
  print("Reading:", csvfile)
  with open(csvfile, 'r') as f:
    reader = csv.DictReader(f)
    rows = []
    for row in reader:
      rows.append((row["date"], row["model"], row["serial_number"], row["failure"],
                   clean(row["smart_9_raw"]), clean(row["smart_241_raw"]),
                   clean(row["smart_242_raw"]), clean(row["smart_193_raw"])))
      if len(rows) & 1024 != 0:
        c.executemany(insert_query, rows)
        affected += c.rowcount
        rows = []
      total += 1
    c.executemany(insert_query, rows)
    affected += c.rowcount
  if total != affected:
    print("  inserted: {}, total: {}".format(affected, total))
  else:
    print("  inserted:", total)
  conn.commit()

def sqlite_first(conn, query):
  c = conn.cursor()
  c.execute(query)
  return c.fetchone()[0]

def main(*args):
  conn = pgs.connect(database='backblaze2', user='john', password='john')
  init(conn)
  if len(args) == 0:
    print("Nothing to import! Number of logs:",
          sqlite_first(conn, "SELECT COUNT(*) FROM raw_logs"))
  else:
    for path in args:
      if os.path.isfile(path):
        csv_import(conn, path)
      else:
        print("Not a file:", path)

if __name__ == '__main__':
  import sys
  main(*sys.argv[1:])
