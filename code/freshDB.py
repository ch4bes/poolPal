import sqlite3

dbFile = '~/poolPal/poolSchedules.db'

# delete former db, it it exists
f = open(dbFile, 'w')
f.close()

# create fresh db
conn = sqlite3.connect(dbFile)
conn.execute('CREATE TABLE schedules (id INTEGER PRIMARY KEY, function TEXT, startTime INTEGER, stopTime INTEGER)')
conn.close()
