#!/usr/bin/python3

###########
# PoolPal #
###########
#########
# Setup #
#########

import sqlite3 as sql
import RPi.GPIO as GPIO
from flask import Flask, render_template, request, redirect, url_for
from schedulerform import SchedulerForm
from conf import *
import datetime, os

if os.path.isfile(sched_db) == False: # if sched_db doesn't exist:
    os.system('sudo python ' + appDir + 'freshDB.py') # run freshDB.py

GPIO.setmode(GPIO.BCM)

# Set each pin as an output and set initial state:
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, pins[pin]['state'])

def timestamp():
    timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
    return timestamp

message = ''

app = Flask(__name__)
app.secret_key = 'development key'

#########
# Flask #
#########

@app.route('/')
def index():
    ip = request.remote_addr
    # For each pin, read the pin state and store it in the pins dictionary:
    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)
    # Put the variables into the template data dictionary:
    templateData = {
        'ip' : ip,
        'pins' : pins,
        'version' : version,
        'message' : message
        }

    # Pass the template data into the template index.html and serve it to the user
    return render_template('index.html', **templateData)

# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route('/<changePin>/<action>')
def action(changePin, action):
    global message
    ip = request.remote_addr
    # Convert the pin from the URL into an integer:
    changePin = int(changePin)
    # Get the device name for the pin being changed
    deviceName = pins[changePin]['name']
    # If the action part of the URL is "on," execute the code indented below:
    if action == 'on':
        # Set the pin high:
        GPIO.output(changePin, GPIO.HIGH)
        # Save the status message to be passed into the template:
        message = 'Turned ' + deviceName + ' on.'
    if action == 'off':
        GPIO.output(changePin, GPIO.LOW)
        message = 'Turned ' + deviceName + ' off.'

    # For each pin, read the pin state and store it in the pins dictionary:
    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)

    # Put the variables into the template data dictionary:
    templateData = {
        'ip' : ip,
        'pins' : pins,
        'version' : version,
        'message' : message
    }

    if ip == pool_pi_ip:
        return render_template('curl.html', **templateData)

    else:
        return redirect('/', code=302)

# Mini Scheduler
@app.route('/scheduler', methods = ['GET', 'POST'])
def scheduler():

    with sql.connect(sched_db) as con:
        cur = con.cursor()
    rows = cur.execute('SELECT * FROM schedules')

    form = SchedulerForm()

    schedules = []
    for row in rows:
        schedules.append(row)
    count = len(schedules)
    if count > 0:
        msg = None
    else:
        msg = 'Nothing currently scheduled'

    templateData = {
        'count': count,
        'msg': msg,
        'form': form,
        'schedules': schedules
    }

    if request.method == 'GET':
        return render_template('scheduler.html', **templateData)

    if request.method == 'POST':
        try:
            print('Try loop started...')
            function = request.form['function']
            startHour = request.form['startHour']
            startMin = request.form['startMin']
            stopHour = request.form['stopHour']
            stopMin = request.form['stopMin']
            print('{}, {}:{}, {}:{}'.format(function, startHour, startMin, stopHour, stopMin))

            cur.execute('INSERT INTO schedules (function, startHour, startMin, stopHour, stopMin) VALUES (?,?,?,?,?)',(function, startHour, startMin, stopHour, stopMin) )
            con.commit()
            msg = 'Record successfully added'

        except:
            con.rollback()
            msg = 'error in insert operation'

        finally:
            con.close()
            # run scheduler.py to add database items to cron
            os.system('sudo python ' + appDir + 'scheduler.py')
            return render_template('result.html', msg = msg)

if __name__ == '__main__':
    try:
        print(timestamp() + ' - Starting server')
        app.run(host='0.0.0.0', port=80, debug=True)
    except KeyboardInterrupt:
        print(timestamp() + ' - Keyboard Interrupt')
    except Exception as e:
        print(e, type(e))
    finally:
        print(timestamp() + ' - cleaning up')
        GPIO.cleanup()
