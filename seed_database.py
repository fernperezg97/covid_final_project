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


headers = {
	"X-RapidAPI-Key": os.environ['RAPID_API_KEY_IN_HEADERS'],
	"X-RapidAPI-Host": os.environ['RAPID_API_HOST_IN_HEADERS']
}

countries = requests.request("GET", url_countries, headers=headers)
countries_dict = countries.json()
country_list = countries_dict.get("response")

# print(countries_dict.get("response"))

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






