import datetime, urllib.request
import sqlite3 as sql
from conf import temp_db, esp_ip

def timestamp():
    #timestamp = datetime.datetime.now()                                                                                          
    timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
    print(str(timestamp))
    return timestamp

def getTemp():
    temp = ''
    attempt_count = 0
    attempts_allowed = 3
    while temp == '' and attempt_count < attempts_allowed:
        print('Getting temp...')
        try:
            with urllib.request.urlopen('http://'+esp_ip) as f:
                result = str(f.read())
                for char in result:
                    if char == '.' or char.isdigit() == True:
                        temp += char
                print(temp)
                return temp
        except Exception as e:
            print(e, type(e))
            attempt_count += 1
            print('Connection errors: ' + str(attempt_count))
            if attempt_count == attempts_allowed:
                return 'No response from ESP32'

def logTemp(timestamp,temp):
    con = sql.connect(temp_db)
    con.row_factory = sql.Row
    cur = con.cursor()
    try:
        cur.execute('INSERT INTO temps (timestamp, temp) VALUES (?,?)',(timestamp,temp))
        con.commit()
        print('record successfully added')
    except:
        print('error in opperation')
        con.rollback()
    finally:
        con.close()

def main():
    ts = timestamp()
    temp = getTemp()
    logTemp(ts,temp)

if __name__ == '__main__':
    main()
