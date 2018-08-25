#!/usr/bin/python3
import os, sqlite3
from conf import sched_db as dbFile

# delete former db, if it exists
f = open(dbFile, 'w')
f.close()

# create fresh db
conn = sqlite3.connect(dbFile)
conn.execute('CREATE TABLE schedules (id INTEGER PRIMARY KEY, function TEXT, startHour INTEGER, startMin INTEGER, stopHour INTEGER, stopMin INTEGER)')
conn.close()
