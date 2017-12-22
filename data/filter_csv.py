#!/bin/env python3

import csv
import os
import sys

def eprint(*args):
  print(*args, file=sys.stderr)

def csv_filter(csvwriter, infile):
  total = 0
  eprint("Reading:", infile)
  with open(infile, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
      csvwriter.writerow(row)
      total += 1
  eprint("  Read", total, "rows.")

def main(outpath, *inpaths):
  if len(inpaths) == 0:
    raise ValueError("At least one input file must be specified")

  # check if the first input file exists before (re)creating the output file
  if not os.path.isfile(inpaths[0]):
    raise ValueError("No such file: " + inpaths[0])

  fieldnames = ["date", "model", "serial_number", "failure",
                "smart_9_raw", "smart_242_raw", "smart_241_raw"]
  with open(outpath, 'w', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fieldnames, extrasaction='ignore')
    for path in inpaths:
      csv_filter(writer, path)

if __name__ == '__main__':
  if len(sys.argv) < 3:
    eprint("Usage:", sys.argv[0], "outfile.csv infile1.csv [infile2.csv ...]")
    sys.exit(1)
  main(*sys.argv[1:])
