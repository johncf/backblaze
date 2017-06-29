import psycopg2 as pgs

def connect():
  return pgs.connect(database='backblaze', user='john', password='john')
