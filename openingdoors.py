#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 23:22:00 2022

@author: Daniel Jimenez
"""
import pandas as pd
import json
import plotly

from flask import Flask
from flask import render_template
from flask import request
from flask import abort
from flask import redirect
from flask import url_for

from api_key import key_exist
from api_key import save_key
from api_key import get_request_counter

from model import process_data
from model import map_plot_property
from model import map_plot
from model import plot_tables
from model import load_states

app = Flask(__name__)



@app.route("/")
def index():
        return render_template("index.html")

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
            call_counter = get_request_counter()
        else:
            _key_exist = "False"
        return render_template("key.html", key_exist=_key_exist, call_counter=call_counter)

@app.route("/search/", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        address = {"address" : request.form['address_input'], "city" : request.form['city_input'],
                        "state" : request.form['state_input'], "zipcode" : request.form['zipcode_input']}
        return redirect(url_for('property_details',**address))
    else:
        if key_exist():
            _key_exist = "True"
            states = load_states()
        return render_template("search.html",key_exist=_key_exist,len=len(states),states=states)

@app.route("/p")
def property_details():
    try:
        address = dict(request.args)
        house_df, sale_df, taxes_df, house_features, house_owner, last_request = process_data(address)
        house = house_df.to_dict(orient="records")
        house = house[0]
        house['price']= "${:,.2f}".format(house['price'])
        date = str(last_request).split(" ")
        date= date[0]
        house_map = map_plot_property(house_df)
        comparables_map =map_plot(sale_df)
        taxes_fig = plot_tables(taxes_df)
        df = sale_df[['address','distance','propertyType','price','bedrooms','bathrooms','squareFootage','lotSize']]
        df.rename(columns = {'address':'Address','distance':'Distance',
                            'propertyType':'Property Type', 'price':'Price',
                            'bedrooms':'Beds', 'bathrooms':'Baths',
                            'squareFootage':'Sqft', 'lotSize':'Lot Size'},inplace=True)
        comparables_fig = plot_tables(df)
        
        graph1 = json.dumps(house_map, cls=plotly.utils.PlotlyJSONEncoder)
        graph2 = json.dumps(comparables_map, cls=plotly.utils.PlotlyJSONEncoder)
        tax_table = json.dumps(taxes_fig, cls=plotly.utils.PlotlyJSONEncoder)
        comparables_table = json.dumps(comparables_fig, cls=plotly.utils.PlotlyJSONEncoder)
        #create the 3 tables with plotly
        return render_template("property_details.html", house_df=house,
                                house_features=house_features,
                                house_owner=house_owner,
                                last_request=date,
                                graph1=graph1,
                                tax_table = tax_table,
                                graph2=graph2,
                                comparables_table = comparables_table)
    except IndexError:
            abort(404)
    except KeyError:
        if len(house_df) == 0: #check if the json has information
            invalid_address = "True"
        else:
            invalid_address = "False"
        return render_template("error.html",invalid_address=invalid_address)