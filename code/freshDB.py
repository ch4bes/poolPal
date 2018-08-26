#!/usr/bin/python3
import os, sqlite3, sys
from conf import sched_db, temp_db

dbFile = sys.argv[1]

# delete former db, if it exists
f = open(dbFile, 'w')
f.close()

conn = sqlite3.connect(dbFile)

if dbFile == sched_db:    
    conn.execute('CREATE TABLE schedules (id INTEGER PRIMARY KEY, function TEXT, startHour INTEGER, startMin INTEGER, stopHour INTEGER, stopMin INTEGER)')
if dbFile == temp_db:
    conn.execute('CREATE TABLE temps (time INTEGER, temp FLOAT)')
    
conn.close()
