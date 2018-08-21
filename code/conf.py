version_prefix = 0
version_suffix = 1
version = version_prefix + version_suffix * .1

print('PoolPal - version ' + str(version))

appDir = '/home/pi/poolPal/code/'
dbFile = appDir + 'poolSchedules.db'

pins = { # Pin Dictionary to store each pin number, name, and state
    17 : {'name':'Light', 'state':1},
    18 : {'name':'Waterfall', 'state':1},
    23 : {'name':'Main Pump', 'state':1},
    27 : {'name':'Gazebo Lights', 'state':1}
    }