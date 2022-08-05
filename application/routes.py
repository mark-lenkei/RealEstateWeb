import statistics
from application import app
from application.data_manager import DataManager
from flask import render_template

rent_manager = DataManager('application/data/rent/*')

@app.route('/')
def home():

    plot_rent, statistics_rent = rent_manager.get_statistics()
    return render_template('home.html', chart_rent=plot_rent, statistics_rent=statistics_rent)