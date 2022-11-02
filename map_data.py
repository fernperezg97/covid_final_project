"""API Data"""

from flask import Flask, render_template, request
from sys import argv
from pprint import pprint, pformat
import json
import requests

# data for timeline map used with scroll bar

url = "https://api.covid19api.com/total/dayone/country/status/confirmed"

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

def get_all_countries(url)
    """loops through all countries and grabs date from first case to current case"""

    for 

# mexico_data_string = open(argv[0]).read()
# mexico_dict = json.loads(mexico_data_string)
# pprint(mexico_dict)


