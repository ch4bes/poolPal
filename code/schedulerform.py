from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
import datetime

hour_choices = []

for i in range(24):
    h = datetime.time(i)
    hour_choices.append((h.strftime('%H'),h.strftime('%-I %p')))

class SchedulerForm(FlaskForm):
    function = SelectField('Function', choices = [
        ('Light','Pool Light'),('Waterfall','Waterfall Pump'),('Main Pump','Main Pump')])
    startTime = SelectField('Start Time', choices = [hour_choices])
    stopTime = SelectField('Stop Time', choices = [hour_choices])
    submit = SubmitField("Send")
