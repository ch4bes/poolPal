version = '0.1'

pool_pi_ip = '127.0.0.1'
esp_ip = '10.0.3.183'

appDir = '/home/pi/poolPal/code/'
sched_db = appDir + 'poolSchedules.db'
temp_db = appDir + 'tempLog.db'

pins = { # Pin Dictionary to store each pin number, name, and initial state
    17 : {'name':'Light', 'state':0},
    18 : {'name':'Waterfall', 'state':0},
    23 : {'name':'Main Pump', 'state':0},
    27 : {'name':'Gazebo Lights', 'state':0}
    }

def main():
    print('PoolPal - version ' + version)

if __name__ == '__main__':
    main()
