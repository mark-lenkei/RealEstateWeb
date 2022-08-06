from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField


class DateIntervalForm(FlaskForm):
    start_date = DateField(label="Start Date")
    end_date = DateField(label="End Date")
    submit = SubmitField(label="Submit")