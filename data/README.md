# Data Directory

Create directories named `2013`, `2014` etc. here and extract corresponding
csv data files into them from Backblaze dataset.

### View Data: `smart_csv2json.py`

This is a convenience script to view a Backblaze csv file as a json list of
objects, where the object key is human-friendly in that it contains a
meaningful name for each SMART value. Example invocation:

    $ cat 2015/2015-01-01.csv | ./smart_csv2json.py | head -n 44
