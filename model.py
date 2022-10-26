#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 23:22:00 2022

@author: Daniel Jimenez
"""
# API post/get
import requests
from api_key import increase_request_counter
# data manipulation
import json
import pandas as pd
import numpy as np



from api_key import get_key


def main():
    """ 
        Does: xxx
        Arguments explanation: xxx
        Return: xxx
    """
    pass

def create_url(endpoint, address, city, state, zipcode):
    """
        Does: takes a full address and makes a resquest url\n
        Arguments:\n
            endpoints : string ['properties', 'salePrice', 'rentalPrice', 'saleListings', 'rentalListings']\n
            The property address, in the format of 'Street, City, State, Zip'.\n
            propertyType : string ['Single Family', 'Condo', 'Townhouse', 'Duplex-Triplex', 'Apartment']\n
            daysOld: integer (The maximum number of days since comparable listings were last seen on the market, with a minimum of 15)\n
            compCount : integer (The number of comparable listings returned by the API, between 5 and 20. Defaults to 5 if not provided)\n
            limit : integer (The maximum number of listings to return, between 1 and 50. Defaults to 50 if not provided)\n
        Return: resquest url based in the desired endpoint
    """
    url = f"https://realty-mole-property-api.p.rapidapi.com/{endpoint}"

    # parameters for value estimate and rent estimate
    # "propertyType":"Single Family","bedrooms":"4","bathrooms":"2","squareFootage":"1600","compCount":"5"
    # parameters for sale listing and rental listing
    # "city":"Austin","state":"TX","limit":"10"

    if endpoint == 'properties':
        querystring = {'address':f'{address}, {city}, {state}, {zipcode}'}
    elif endpoint == 'salePrice' or endpoint == 'rentalPrice':
        querystring = {'address':f'{address}, {city}, {state}, {zipcode}',"propertyType":{}, "bedrooms":{},"bathrooms":{},"squareFootage":{},"daysOld":{},"compCount":{}}
    elif endpoint == 'saleListings' or endpoint == 'rentalListings':
        querystring = {"city":{city},"state":{state},"limit":{}}

    headers = {
	    "X-RapidAPI-Key": get_key(),
	    "X-RapidAPI-Host": "realty-mole-property-api.p.rapidapi.com"
        }

    request_url = f'"GET", {url}, headers={headers}, params={querystring}'
    #response = requests.request("GET", url, headers=headers, params=querystring)
    return request_url

def api_request(request_url):
    with requests.request(request_url) as session:
        data = session.text
        increase_request_counter()
    return data

if __name__ == "__main__":
    print(create_url("properties", "5500 Grand Lake Dr", "San Antonio", "TX", 78244))
    