"""Server for COVID-19 Final Project"""

from flask import (Flask, render_template, request, flash, session, redirect)
import json
import requests
# import crud
# import jinga2
from jinja2 import StrictUndefined

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

@app.route("/ex")
def ex():
    """View ex html."""

    return render_template("ex.html")






if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")