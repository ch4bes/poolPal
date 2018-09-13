import sqlite3 as sql
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from conf import temp_db

window = 3 # how many values to include in running avg calculation (3 seems to be the sweet spot)

def get_avg(value,other,n):
    total = 0
    for item in other:
        total += item # add up values in [other]
    avg = (value+total)/n # get [avg] by <adding [value] to [total]> and <dividing by number [n] of values being added>
    if len(other) == window-1: # if there are too many values in [other]:
        del other[0]           # delete the oldest value in [other]
    other.append(avg) # add most recently calculated [avg] to [other]
    return avg

def running_avg(data,window):
    other = [] # holds values used in avg calculation
    y2 = [] # holds calculated averages
    off_by = [] # holds values of how far off the calculated avg is from the actual recorded temperature values
    n = 0
    for value in data: # for every temperature [value] in [data]:
        if n < window: # if item counter [n] is smaller than the set [window] value:
            n += 1     # add one unit to the counter [n]
        avg = get_avg(value,other,n) # pass variables to get_avg() function
        y2.append(avg) # add newly calculated [avg] to [y2]
        off_by.append(value-avg) # calculate how far off the [avg] is from actual [value]
    return y2,off_by

#def running_avg(values):
#    y2 = []
#    first = True
#    second = True
#    for value in values:
#        if first == True:
#            avg = value
#            first = avg
#        elif second == True:
#            avg = (value+first)/2
#            #second = value #      <~~~~~~~~~~~~~~~~~~\#
#            second = avg # use [avg] instead of [value]
#        else:             # to smooth running avg     #
#            avg = (value+first+second)/3              #
#            first = second                            #
#            #second = value #      <~~~~~~~~~~~~~~~~~~/#
#            second = avg  #       <~~~~~~~~~~~~~~~~~/#

#        y2.append(avg)
#    return y2

#def smooth_running_avg(values):
#    y2 = []
#    first = True
#    second = True
#    for value in values:
#        if first == True:
#            avg = value
#            first = avg
#        elif second == True:
#            avg = (value+first)/2
#            second = value #      <~~~~~~~~~~~~~~~~~~\#
#            #second = avg # use [avg] instead of [value]
#        else:             # to smooth running avg     #
#            avg = (value+first+second)/3              #
#            first = second                            #
#            second = value #      <~~~~~~~~~~~~~~~~~~/#
#            #second = avg  #       <~~~~~~~~~~~~~~~~~/#
#
#        y2.append(avg)
#    return y2

class Plot():                                 #            (0)date (1)time
                                              #             (0 1 2) (0 1)
    def __init__(self, start=None, end=None): # start/end: ((y,m,d),(h,m))
        try:
            # parse & set datetime values
            self.start = start
            
            self.start_date = self.start[0]
            self.start_year = self.start_date[0]
            self.start_month = self.start_date[1]
            self.start_day = self.start_date[2]

            self.start_time = self.start[1]
            self.start_hour = self.start_time[0]
            self.start_min = self.start_time[1]

            self.end = end

            self.end_date = self.end[0]
            self.end_year = self.end_date[0]
            self.end_month = self.end_date[1]
            self.end_day = self.end_date[2]

            self.end_time = self.end[1]
            self.end_hour = self.end_time[0]
            self.end_min = self.end_time[1]
#        except AttributeError:
#            print('AttributeError')
        except TypeError: # if TypeError is thrown (if start == None type):
            print('No start value\nUsing entire database') # Let user know that entire database will be used

    def get_values(self):
        raw_x = [] # list for storing human readable datetime strings
        x = [] # list for datetime values
        y = [] # list for temperature values
        # ^^^  # each list should have the same amount of entries

        con = sql.connect(temp_db) # connect to temperature database located at [temp_db] path
        con.row_factory = sql.Row
        cur = con.cursor()

        if self.start == None: # if no start value specified
            rows = cur.execute('SELECT * FROM temps') # get all values from temp_db
        else:
            rows = cur.execute( # get specific range of entries from temp_db
                'SELECT * FROM temps WHERE timestamp >= \''
                + self.start_year + '-' + self.start_month + '-' + self.start_day + ' '
                + self.start_hour + ':' + self.start_min + '\' AND timestamp <= \''
                + self.end_year + '-' + self.end_month + '-' + self.end_day + ' '
                + self.end_hour + ':' + self.end_min + '\'')

        for row in rows: # for row gathered from database
            raw_x_val = row[0] # get raw_x value
            x_mod = mdates.datestr2num(row[0]) # change raw_x value into a floating point number
            raw_y = row[1] # get temperature value
            if raw_y == 'No response from ESP32': # if we get a no-response message: 
                raw_y = 0 # since an integer is needed, set y value to 0
                
            raw_x.append(raw_x_val) # add human-readable string to [raw_x]
            x.append(x_mod) # add datetime float value to [x]
            y.append(raw_y) # add temperatue value to [y]

        return (raw_x,x,y)

    def draw_plot(self):
        raw_x,x,y = self.get_values() # get x and y values
        y2,off_by = running_avg(y,window) # get y2 values with running_avg() function
        #y3 = smooth_running_avg(y)
        for item in range(len(x)): # for number of items in list [x], print values of each list (not just list [x])
            print('\nraw_x: ' + raw_x[item] + '\tx: ' + str(x[item]) + '\t y: ' + str(y[item]) + '\t y2: ' + str(y2[item]))

        plt.ion() # turn interactive mode on
        plt.clf() # clear the current figure
        #plt.scatter(x,y)
        plt.plot_date(x,y) # plot temperatue values by datetime value (datetime scatter plot)
        plt.plot(x,y2, color='green', linewidth=5.0) # plot calculated average across same x axis (line plot)
        #plt.plot(x,y3, color='red', linewidth=1.0)
        plt.xlabel('time')
        plt.ylabel('temp. (f)')
        plt.draw() # draw plot to screen
        #plt.show()  # seems to work like plt.draw()

#    def save_plot(self):
#        #plt.ion()
#        x,y = self.get_values()
#        plt.clf()
#        plt.scatter(x,y)
#        plt.plot_date(x,y,)
#        plt.savefig('static/images/plot.png')

class Last():
    def __init__(self):
        def last(days=None, hours=None, mins=None):
            time_now = dt.datetime.now() # get current datetime
            if days != None: # if there's a [days] value:
#                print('days!\t' + str(days))
                time_ago = time_now - dt.timedelta(days=days) # get [time_ago] from amnt of [days] before [time_now]
            elif hours != None: # if there's a [hours] value:
                time_ago = time_now - dt.timedelta(hours=hours) # get [time_ago] from amnt of [hours] before [time_now]
            elif mins != None: # if there's a [mins] value:
                time_ago = time_now - dt.timedelta(minutes=mins) # get [time_ago] from amnt of [mins] before [time_now]

            sy = time_ago.strftime('%Y') # start year
            sm = time_ago.strftime('%m') # start month
            sd = time_ago.strftime('%d') # start day
            sH = time_ago.strftime('%H') # start hour
            sM = time_ago.strftime('%M') # start minute

            ey = time_now.strftime('%Y') # end year
            em = time_now.strftime('%m') # end month
            ed = time_now.strftime('%d') # end day
            eH = time_now.strftime('%H') # end hour
            eM = time_now.strftime('%M') # end minute

            start = ((sy,sm,sd),(sH,sM)) # start tuple: ((date tuple),(time tuple))
            end = ((ey,em,ed),(eH,eM))   # end tuple

            return start,end

        units = input('Which units to use? (pick one) (d)ays, (h)ours, (m)ins: ') # set units from user input
        amnt = input('How many back?: ') # set amount of chosen unit from user input
        if units == 'd' or units == 'days': # if [units] chosen is [days]:
            self.start,self.end = last(days=int(amnt)) # set self.start/end by passing [days] int to last() function
        elif units == 'h' or units == 'hours': # if [units] chosen is [hours]:
            self.start,self.end = last(hours=int(amnt)) # set self.start/end by passing [hours] int to last() function
        elif units == 'm' or units == 'minutes': # if [units] chosen is [minutes]:
            self.start,self.end = last(mins=int(amnt)) # set self.start/end by passing [minutes] int to last() function

last1 = Last() # set [last1] variable to an instance of Last() class
print(last1.start) # print start tuple of start date and start time
plot1 = Plot(last1.start,last1.end) # set [plot1] variable to an instance of Plot() class, using range from [last1]

#start = (('2018','09','03'),('12','00'))
#end = (('2018','09','03'),('22','00'))
#plot1 = Plot(start,end)

#plot2 = Plot()

plot1.draw_plot() # draw [plot1]
#plot1.save_plot() # need to edit save_plot() function
