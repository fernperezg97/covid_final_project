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

url = "https://api.covid19api.com/countries"

payload = {}
headers = {}

rows = len(model.Country.query.all())
countries = requests.request("GET", url, headers=headers, data=payload)

while (rows != 248):
    while (countries.status_code != 200):
        countries = requests.request("GET", url, headers=headers, data=payload)
        print(f"Countries status code: {countries.status_code}")
        time.sleep(5)

    countries_dict = countries.json()
    print(f"\n\nSTATUS: ({countries})\n\n")

    for country in countries_dict:
        print(f"Type: {type(country)} - Country: {country}")
        country_name = country.get("Country")
        print(f"Country Name: {country_name}\n")
        input()
    
        # country_slug = country.get("Slug")
        # country_id = country.get("ISO2")
        # country_instance = crud.create_country(country_name, country_slug, country_id)
        # print(f"I'm adding country: {country_name}")
        # model.db.session.add(country_instance)
    model.db.session.commit()
    time.sleep(1)
    rows = len(model.Country.query.all())

print(model.Country.query.all())


# print(f"These are the countries: {countries} \n\n\n")
# print(f"#########  There are this many countries: {len(countries_dict)}\n\n\n")
# print(f"This is the countries' dictionary: {countries_dict}")



