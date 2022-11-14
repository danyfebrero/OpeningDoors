#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 23:22:00 2022

@author: Daniel Jimenez
"""
import pandas as pd

from flask import Flask
from flask import render_template
from flask import request
from flask import abort
from flask import redirect
from flask import url_for

from api_key import key_exist
from api_key import save_key

from model import process_data
from model import map_plot


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        address = request.form['address_input']
        return redirect(url_for('property_details',address=address))
    else:
        if key_exist():
            _key_exist = "True"
        else:
            _key_exist = "False"
        return render_template("index.html", key_exist=_key_exist)

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/api_key/", methods=["GET", "POST"])
def api_key():
    if request.method == "POST":
        key = request.form['key']
        save_key(key)
        return redirect(url_for('index'))
    else:
        if key_exist():
             _key_exist = "True"
        else:
            _key_exist = "False"
        return render_template("key.html", key_exist=_key_exist)

@app.route("/p/<string:address>", methods=["GET", "POST"])
def property_details(address):
    if request.method == "POST":
        address = request.form['address_input']
        address = {}
        return redirect(url_for('property_details', address=address))
    else:
        try:
            _location = ""
            _address = address #transform the address to the correct format
            _endpoints = [] # get from the check box in the html
            last_request, property_data, property_comps, property_rent = process_data(_location,_address,_endpoints)
            df_prop = pd.DataFrame.from_dict(property_data)
            property_map = map_plot(df_prop,property_data['addressLine1'])
            return render_template("property_details.html", last_request=last_request, 
                                    property_data=property_data, property_comps=property_comps, 
                                    property_rent=property_rent)
        except IndexError:
            abort(404)
        except KeyError:
            if len(property_data) == 0: #check if the json has information
                invalid_address = "True"
            else:
                invalid_address = "False"
            return render_template("error.html",invalid_address=invalid_address)