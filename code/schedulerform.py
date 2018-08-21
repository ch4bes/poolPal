from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from conf import pins
import datetime

function_choices = []

for pin in pins:
    choice = (pins[pin]['name'],pins[pin]['name'])
    function_choices.append(choice)

hour_choices = []
min_choices = []

for i in range(24):
    h = datetime.time(i)
    value = h.strftime('%H')
    label = h.strftime('%-I %p')
    choice = (value,label)
    hour_choices.append(choice)

for i in range(4):
    n = i*15
    m = datetime.time(0,n)
    value = m.strftime('%M')
    label = value
    choice = (value, label)
    min_choices.append(choice)

class SchedulerForm(FlaskForm):
    function = SelectField('Function', choices = function_choices)
    startHour = SelectField('Hour', choices = hour_choices)
    startMin = SelectField('Minute', choices = min_choices)
    stopHour = SelectField('Hour', choices = hour_choices)
    stopMin = SelectField('Minute', choices = min_choices)
    submit = SubmitField("Send")
