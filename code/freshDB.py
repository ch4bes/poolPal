#!/usr/bin/python3
import os, sqlite3

# get proper home directory
user = os.getenv('SUDO_USER')
home = '/home/' + user

dbFile = home + '/poolPal/code/poolSchedules.db'

# delete former db, if it exists
f = open(dbFile, 'w')
f.close()

# create fresh db
conn = sqlite3.connect(dbFile)
conn.execute('CREATE TABLE schedules (id INTEGER PRIMARY KEY, function TEXT, startTime INTEGER, stopTime INTEGER)')
conn.close()
