#!/bin/python3

import sqlite3
import csv
import os

def init(conn):
  c = conn.cursor()
  c.execute('''CREATE TABLE IF NOT EXISTS raw_logs
               (date DATE,        model TEXT,       serial TEXT,      failed BOOLEAN,
                poh INTEGER,      lba_w INTEGER,    lba_r INTEGER,    load_cc INTEGER)''')
  c.execute('''CREATE UNIQUE INDEX IF NOT EXISTS raw_logs_uniq on raw_logs (date, serial)''')
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
  insert_query = '''INSERT OR IGNORE INTO raw_logs (date, model, serial, failed,
                                                    poh,  lba_w, lba_r,  load_cc)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
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
    print("  inserted:{}, total:{}".format(affected, total))
  else:
    print("  inserted:", total)
  conn.commit()

def sqlite_first(conn, query):
  c = conn.cursor()
  c.execute(query)
  return c.fetchone()[0]

def main(*args):
  conn = sqlite3.connect('backblaze.db')
  init(conn)
  if len(args) == 0:
    print("Nothing to import! Number of logs:",
          sqlite_first("SELECT COUNT(*) FROM raw_logs"))
  else:
    for path in args:
      if os.path.isfile(path):
        csv_import(conn, path)
      else:
        print("Not a file:", path)

if __name__ == '__main__':
  import sys
  main(*sys.argv[1:])
