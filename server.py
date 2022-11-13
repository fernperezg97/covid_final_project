"""Server for COVID-19 Final Project"""

from flask import (Flask, render_template, request, flash, session, redirect, jsonify)
import json
import requests
import crud
# import jinga2
import os
from updated_keys import new_keys
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





@app.route("/login")
def login():
    """View login page."""

    return render_template("login.html")


@app.route("/register")
def register():
    """View register page when user clicks create account."""

    return render_template("register.html")


@app.route("/user-registration-info", methods=["POST"])
def user_info_to_database():
    """Send user input to database."""

    firstName = request.json['firstName']
    lastName = request.json['lastName']
    email = request.json['email']
    password = request.json['password']

    crud.create_user_instance(firstName, lastName, email, password)

    return ""


@app.route("/user-login-info", methods=["POST"])
def validate_user():
    """Check if user exists in database."""

    email = request.json['email']
    password = request.json['password']

    user_validation = crud.check_if_user_in_system(email, password)

    if user_validation is None:
        return render_template("login.html")
    else:
        return render_template("timeline.html")
    


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

    date_query_string = request.args.get("date") # grabs client date input on slider

    cases_for_all_countries_by_date = crud.get_country_cases_by_date(date_query_string) # returns a list of tuples w/ countries and cases
    dict_cases_by_country = dict(cases_for_all_countries_by_date) # convert that list of tuples to a dictionary w/ multiple "key":value pairs bc you can't pass in a tuple to js

    original_keys_list = list(dict_cases_by_country.keys())

    for key in original_keys_list:
        if (key in new_keys):
            dict_cases_by_country[new_keys[key]] = dict_cases_by_country.pop(key)


    print(dict_cases_by_country)

    return dict_cases_by_country



if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, host="0.0.0.0")