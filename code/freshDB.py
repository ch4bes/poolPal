#!/usr/bin/python3
import os, sqlite3
from conf import dbFile

# delete former db, if it exists
f = open(dbFile, 'w')
f.close()

# create fresh db
conn = sqlite3.connect(dbFile)
conn.execute('CREATE TABLE schedules (id INTEGER PRIMARY KEY, function TEXT, startTime INTEGER, stopTime INTEGER)')
conn.close()
