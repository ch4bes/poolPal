from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

class SchedulerForm(FlaskForm):

    function = SelectField('Function', choices = [
        ('Light','Pool Light'),('Waterfall','Waterfall Pump'),('Main Pump','Main Pump')])

    startTime = SelectField('Start Time', choices = [
        ('00','12am'),('01','1am'),('02','2am'),('03','3am'),('04','4am'),('05','5am'),('06','6am'),
        ('07','7am'),('08','8am'),('09','9am'),('10','10am'),('11','11am'),('12','12pm'),
        ('13','1pm'),('14','2pm'),('15','3pm'),('16','4pm'),('17','5pm'),('18','6pm'),
        ('19','7pm'),('20','8pm'),('21','9pm'),('22','10pm'),('23','11pm')])

    stopTime = SelectField('Stop Time', choices = [
        ('00','12am'),('01','1am'),('02','2am'),('03','3am'),('04','4am'),('05','5am'),('06','6am'),
        ('07','7am'),('08','8am'),('09','9am'),('10','10am'),('11','11am'),('12','12pm'),
        ('13','1pm'),('14','2pm'),('15','3pm'),('16','4pm'),('17','5pm'),('18','6pm'),
        ('19','7pm'),('20','8pm'),('21','9pm'),('22','10pm'),('23','11pm')])

    submit = SubmitField("Send")
