#!/bin/python3

import sqlite3
import csv

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
    print("total != affected :", total, "!=", affected)
  else:
    print("inserted:", total)
  conn.commit()

conn = sqlite3.connect('backblaze.db')

init(conn)
csv_import(conn, '/home/john/Downloads/backblaze/2014/2014-05-01.csv')
