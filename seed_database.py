"""Script to seed database"""

import os
import json
from random import choice, randint
from datetime import datetime
import requests
import crud
import model
import server
import time

os.system('dropdb covid')
os.system('createdb covid')

model.connect_to_db(server.app)
model.db.create_all()


"""Grab all countries from API"""

url_countries = "https://covid-193.p.rapidapi.com/countries"
url_history = "https://covid-193.p.rapidapi.com/history"
url_statistics = "https://covid-193.p.rapidapi.com/statistics"


headers = {
	"X-RapidAPI-Key": os.environ['RAPID_API_KEY_IN_HEADERS'],
	"X-RapidAPI-Host": os.environ['RAPID_API_HOST_IN_HEADERS']
}

countries = requests.request("GET", url_countries, headers=headers)
countries_dict = countries.json()
country_list = countries_dict.get("response")


country_stats = requests.request("GET", url_statistics, headers=headers)
country_stats_dict = country_stats.json()
country_stats_list = country_stats_dict.get("response")


for country in country_stats_list:
    country_name = country["country"]
    population = country["population"]
    total_cases_stats = country["cases"]["total"]
    cases_1m = country["cases"]["1M_pop"]
    active_cases = country["cases"]["active"]
    total_deaths_stats = country["deaths"]["total"]
    deaths_1m = country["deaths"]["1M_pop"]
    total_tests = country["tests"]["total"]
    tests_1m = country["tests"]["1M_pop"]
    print(f"CONTENT: ", country_name, population, total_cases_stats, cases_1m, active_cases, total_deaths_stats, deaths_1m, total_tests, tests_1m)
    if country_name == "All":
        continue
    country_stats_instance = crud.create_country_stats_instance(country_name, population, total_cases_stats, cases_1m, active_cases, total_deaths_stats, deaths_1m, total_tests, tests_1m)
    model.db.session.add(country_stats_instance)





for country in country_list:
    country_instance = crud.create_country(country)
    model.db.session.add(country_instance)
    querystring = {"country":country}
    dates_and_cases_by_country = requests.request("GET", url_history, headers=headers, params=querystring)
    dates_and_cases_by_country_dict = dates_and_cases_by_country.json()
    dates_and_cases_by_country_list = dates_and_cases_by_country_dict.get("response")
    date = 0
    for dictionary in dates_and_cases_by_country_list:
        # if date doesn't match previously stored date, add new date and cases to database (AND DEATHS)
        if date != dictionary["day"]:
            date = dictionary["day"]
            total_cases = dictionary["cases"]["total"]
            total_deaths = dictionary["deaths"]["total"]
            country_id = crud.get_id_by_country_name(country)
            covid_record_instance = crud.create_covid_record(country_id, date, total_cases, total_deaths)
            model.db.session.add(covid_record_instance)

model.db.session.commit()






