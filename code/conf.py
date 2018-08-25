version = '0.1'

print('PoolPal - version ' + version)

pool_pi_ip = '127.0.0.1'
esp_ip = '10.0.3.183'

appDir = '/home/pi/poolPal/code/'
sched_db = appDir + 'poolSchedules.db'
temp_db = appDir + 'tempLog.db'

pins = { # Pin Dictionary to store each pin number, name, and state
    17 : {'name':'Light', 'state':1},
    18 : {'name':'Waterfall', 'state':1},
    23 : {'name':'Main Pump', 'state':1},
    27 : {'name':'Gazebo Lights', 'state':1}
    }
