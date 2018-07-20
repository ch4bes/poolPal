import sqlite3 as sql
from crontab import CronTab
import os, datetime

cron = CronTab('root')

home = '/home/pi'

con = sql.connect(home + '/poolPal/code/poolSchedules.db')
con.row_factory = sql.Row

cur = con.cursor()
cur.execute('select * from schedules')

rows = cur.fetchall()

print('Accessing Database...\n\nDatabase Items:\n')
for index, row in enumerate(rows):

    id = 'pool' + str(row[0])
    function = str(row[1])
    startTime = datetime.time(row[2]).strftime('%I %p')
    stopTime = datetime.time(row[3]).strftime('%I %p')

    if function == 'Light':
        pin = 17
    elif function == 'Waterfall':
        pin = 18
    elif function == 'Main Pump':
        pin = 23
    
    print(str(index + 1) + ' - ' + function + '(pin ' + str(pin) + ') will turn on at ' + startTime + ' and turn off at ' + stopTime + ' (id=' + id + ')')
    
    # check for job by comment
    list = cron.find_comment(id)
    # print search
    print('\n\tsearching by comment: ' + id)

    # check if list is empty
    if not sorted(list):

        ## start ##
        print('\n\tcreating start script')
        # make script for start function (/<pin>/on)
        onscript = '/usr/local/bin/pool/' + str(pin) + '_on.sh'
        f = open(onscript,"w")
        f.write('curl http://pool.local/' + str(pin) + '/on')
        f.close()

        print('\tadding execute permission')
        # chmod +x
        os.system('sudo chmod +x ' + onscript)

        print('\tadding start job to cron')
        # make cronjob for start function
        job = cron.new(command=('sudo bash ' + onscript + ' >> /var/log/poolcronlog.log 2>&1'),comment=id)
        job.minute.on(0)
        job.hour.on(row[2]) # startTime = row[2]
        job.enable()
        cron.write()
        print('\tadded')

        ## stop ##
        print('\n\tcreating stop script')
        # make script for stop function (/<pin>/off)
        offscript = '/usr/local/bin/pool/' + str(pin) + '_off.sh'
        f = open(offscript,"w")
        f.write('curl http://pool.local/' + str(pin) + '/off')
        f.close()

        print('\tadding execute permission')
        # chmod +x
        os.system('sudo chmod +x ' + offscript)

        print('\tadding stop job to cron')
        # make cronjob for stop function
        job = cron.new(command=('sudo bash ' + offscript + ' >> /var/log/poolcronlog.log 2>&1'),comment=id)
        job.minute.on(0)
        job.hour.on(row[3]) # stopTime = row[3]
        job.enable()
        cron.write()
        print('\tadded')

        print('\n\tscheduled ' + function + ' to turn on at ' + startTime + '\n\tscheduled ' + function + ' to turn off at ' + stopTime)

    else:
        print('\t\tfound scheduled item' + '\n')

print('\nAll functions scheduled')
