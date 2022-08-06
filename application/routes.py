from application import app
from application.data_manager import DataManager
from application.forms import DateIntervalForm
from flask import render_template

rent_manager = DataManager('application/data/rent/*')

@app.route('/', methods=['GET', 'POST'])
def home():
    form = DateIntervalForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
        plot_rent, statistics_rent = rent_manager.get_statistics(start_date, end_date)
        return render_template('home.html', chart_rent=plot_rent, statistics_rent=statistics_rent, form=form)

    plot_rent, statistics_rent = rent_manager.get_statistics()
    return render_template('home.html', chart_rent=plot_rent, statistics_rent=statistics_rent, form=form)