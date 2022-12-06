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
app.secret_key = os.environ['API_KEY']

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.
app.jinja_env.undefined = StrictUndefined

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True


@app.route("/")
def login_homepage():
    """Homepage is now login page."""

    return render_template("login.html")




@app.route("/login")
def login():
    """View login page."""

    return render_template("login.html")




@app.route("/register")
def register():
    """View register page when user clicks create account."""

    return render_template("register.html")




@app.route("/user-registration-check", methods=['POST', 'GET'])
def registration_duplicates_check():
    """Check if user exists in database."""

    email = request.json['email']
    password = request.json['password']
    firstName = request.json['firstName']
    lastName = request.json['lastName']

    user_exists = crud.check_if_user_in_system(email, password)

    if user_exists is None and not '' in [firstName, lastName, email, password]:
        crud.create_user_instance(firstName, lastName, email, password)
    
        return {"result": "sucessful", "status": "LOGIN WITH YOUR NEW CREDENTIALS."}
    else:
        return {"result": "unsuccessful", "status": "USER ALREADY EXISTS OR CREDENTIALS INVALID."}




@app.route("/user-registration-info", methods=["POST"])
def user_info_to_database():
    """Send user input to database."""

    firstName = request.json['firstName']
    lastName = request.json['lastName']
    email = request.json['email']
    password = request.json['password']

    crud.create_user_instance(firstName, lastName, email, password)
    # print("I got here.")
    return render_template("login.html")




@app.route("/user-login-info", methods=["POST"])
def validate_user():
    """Check if user exists for login using email and password."""

    email = request.json['email']
    password = request.json['password']

    user_validation = crud.check_if_user_in_system(email, password)

    if user_validation is None:
        # print("User Not Found")
        return {"result": "unsuccessful", "status": "EMAIL OR PASSWORD INCORRECT. PLEASE TRY AGAIN."}
    else:
        session['name'] = user_validation.first_name
        session['user_id'] = user_validation.user_id
        # print(session['name'], session['user_id'])
        return {"result": "successful"}




@app.route("/save-recent-date", methods=["POST"])
def save_recent_date():
    """Saves the last date a user chose on slider, so that it appears when they next login."""

    user_id = session['user_id']
    date_before_logout = request.json.get("dateBeforeLogout")
    
    recent_date_by_user_id = crud.save_recent_date(user_id, date_before_logout)

    return ""




@app.route('/check-recent-date')
def check_recent_date_chosen():
    """Check if there exists a recent date based on user ID."""

    user_id = session['user_id']
    recent_chosen_date_and_name = crud.check_if_user_has_recent_date(user_id)

    return recent_chosen_date_and_name

      


@app.route("/covid-timeline")
def covid_timeline():
    """View timeline from case 1 to present."""


    return render_template("timeline.html")




@app.route("/country-search")
def country_search_result():
    """View country_search_result.html page when user types country and hits search button."""

    return render_template("country_search_result.html")




@app.route("/api/get-country-search-stats")
def country_search_stats():
    """Return the statistics of a particular country when searched."""

    country_search_name = request.args.get("country") # grabs user country search input
    country_search_stats = crud.stats_per_country(country_search_name)

    return jsonify(country_search_stats)




@app.route("/api/get-line-graph-stats")
def line_graph_stats():
    """Returns the total cases and total deaths for user searched country."""

    tuple_dates = []
    tuple_cases = []
    tuple_deaths = []
    dict_for_line_graph = {}

    line_graph_country_name = request.args.get("country") # uses user country search input to update line graph cases and deaths
    line_graph_cases_deaths_by_country = crud.cases_and_deaths_for_chosen_country(line_graph_country_name) # query returns list of tuples (country, datetime, cases, deaths)
    line_graph_cases_deaths_by_country.reverse()

    for tup in line_graph_cases_deaths_by_country:
        tuple_dates.append(str(tup[1]))
        tuple_cases.append(tup[2])
        tuple_deaths.append(tup[3])

    dict_for_line_graph = {"dates": tuple_dates, "cases": tuple_cases, "deaths": tuple_deaths}
    print(dict_for_line_graph)


    return dict_for_line_graph




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


    # print(dict_cases_by_country)

    return dict_cases_by_country




@app.route("/api/get-deaths-by-date")
def get_deaths_by_date():
    """Returns the total deaths for a all countries by chosen date."""

    date_query_string = request.args.get("date") # grabs client date input on slider

    deaths_for_all_countries_by_date = crud.get_country_deaths_by_date(date_query_string) # returns a list of tuples w/ countries and deaths
    dict_deaths_by_country = dict(deaths_for_all_countries_by_date) # convert that list of tuples to a dictionary w/ multiple "key":value pairs bc you can't pass in a tuple to js

    original_keys_list = list(dict_deaths_by_country.keys())

    for key in original_keys_list:
        if (key in new_keys):
            dict_deaths_by_country[new_keys[key]] = dict_deaths_by_country.pop(key)


    # print(dict_deaths_by_country)

    return dict_deaths_by_country



if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, host="0.0.0.0")