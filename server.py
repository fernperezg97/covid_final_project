"""Server for COVID-19 Final Project"""

from flask import (Flask, render_template, request, flash, session, redirect, jsonify)
import json
import requests
import crud
# import jinga2
import os

from jinja2 import StrictUndefined
from model import connect_to_db, db




app = Flask(__name__)

# A secret key is needed to use Flask sessioning features
app.secret_key = "covid_sucks_butt"

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.
app.jinja_env.undefined = StrictUndefined

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True





@app.route("/")
def homepage():
    """View Homepage."""

    return render_template("homepage.html")

@app.route("/covid-timeline")
def covid_timeline():
    """View timeline from case 1 to present."""

    # total = crud.get_total_num_dates()
    # print(total)

    return render_template("timeline.html")

@app.route("/api/get-list-days")
def get_list_of_days():
    """Return dictionary containing total number of unique days and a list of unique dates as JSON."""

    list_of_days = crud.get_list_of_days()
    dict_num_days_and_all_dates = {
        "total_unique_days": len(list_of_days), 
        "list_unique_dates": list_of_days}

    return jsonify(dict_num_days_and_all_dates)

@app.route("/api/get-cases-by-date")
def get_cases_by_date():
    """Returns the total cases for a all countries by chosen date."""

    date_queried = request.args.get('date')

    cases_for_all_countries_by_date = crud.get_country_cases_by_date(date_queried)
    # print(cases_for_all_countries_by_date)

    return cases_for_all_countries_by_date



if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, host="0.0.0.0")