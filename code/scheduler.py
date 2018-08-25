import sqlite3 as sql
from crontab import CronTab
import os, datetime
from conf import pins, appDir, sched_db

cron = CronTab('root')

con = sql.connect(sched_db)
con.row_factory = sql.Row

cur = con.cursor()
cur.execute('select * from schedules')

rows = cur.fetchall()

print('Accessing Database...\n\nDatabase Items:\n')
for index, row in enumerate(rows):

    id = 'pool' + str(row[0])
    function = str(row[1])
    startHour = datetime.time(row[2]).strftime('%I %p')
    startMin = datetime.time(0,row[3]).strftime('%M')
    startTime = datetime.time(row[2],row[3]).strftime('%I:%M %p')
    stopHour = datetime.time(row[4]).strftime('%I %p')
    stopMin = datetime.time(0,row[5]).strftime('%M')
    stopTime = datetime.time(row[4],row[5]).strftime('%I:%M %p')

    for key, value in pins.items():
        if value['name'] == function:
            pin = key

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
        onscript = appDir + str(pin) + '_on.sh'
        if os.path.isfile(onscript) == False:
            print('\t' + onscript + ' does not exist. Creating..')
            f = open(onscript,"w")
            f.write('curl http://pool.local/' + str(pin) + '/on')
            f.close()

            print('\tadding execute permission')
            os.system('sudo chmod +x ' + onscript)

        print('\tadding start job to cron')
        # make cronjob for start function
        job = cron.new(command=('sudo bash ' + onscript + ' >> /var/log/poolcronlog.log 2>&1'),comment=id)
        job.minute.on(row[3])
        job.hour.on(row[2])
        job.enable()
        cron.write()
        print('\tadded')

        ## stop ##
        print('\n\tcreating stop script')
        # make script for stop function (/<pin>/off)
        offscript = appDir + str(pin) + '_off.sh'
        if os.path.isfile(offscript) == False:
            print('\t' + offscript + ' does not exist. Creating..')
            f = open(offscript,"w")
            f.write('curl http://pool.local/' + str(pin) + '/off')
            f.close()

            print('\tadding execute permission')
            os.system('sudo chmod +x ' + offscript)

        print('\tadding stop job to cron')
        # make cronjob for stop function
        job = cron.new(command=('sudo bash ' + offscript + ' >> /var/log/poolcronlog.log 2>&1'),comment=id)
        job.minute.on(row[5])
        job.hour.on(row[3])
        job.enable()
        cron.write()
        print('\tadded')

        print('\n\tscheduled ' + function + ' to turn on at ' + startTime + '\n\tscheduled ' + function + ' to turn off at ' + stopTime + '\n')

    else:
        print('\t\tfound scheduled item' + '\n')

print('\nAll functions scheduled')
