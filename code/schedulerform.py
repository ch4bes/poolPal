from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
import datetime

hour_choices = []
min_choices = []

for i in range(24):
    h = datetime.time(i)
    hour_choices.append((h.strftime('%H'),h.strftime('%-I %p')))
    
for i in range(4):
    n = i*15
    m = datetime.time(0,n)
    min_choices.append((str(i),m.strftime('%M')))

class SchedulerForm(FlaskForm):
    function = SelectField('Function', choices = [
        ('Light','Pool Light'),('Waterfall','Waterfall Pump'),('Main Pump','Main Pump')])
    startHour = SelectField('Start Hour', choices = [hour_choices])
    startMin = SelectField('Minute', choices = [min_choices])
    stopHour = SelectField('Stop Hour', choices = [hour_choices])
    stopMin = SelectField('Minute', choices = [min_choices])
    submit = SubmitField("Send")
