#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 23:22:00 2022

@author: Daniel Jimenez
"""
# API post/get
from turtle import position
import requests

# data manipulation
import json
import pandas as pd
import numpy as np

from api_key import get_key
from api_key import increase_request_counter


def create_url(endpoint, address, city, state, zipcode, squareFootage=None, 
                bathrooms=None, bedrooms=None, propertyType=None, compCount=5, limit=None):
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
        querystring = {'address':f'{address}, {city}, {state}, {zipcode}',"propertyType":{propertyType}, "bedrooms":{bedrooms},"bathrooms":{bathrooms},"squareFootage":{squareFootage},"daysOld":{},"compCount":{compCount}}
    elif endpoint == 'saleListings' or endpoint == 'rentalListings':
        querystring = {"city":{city},"state":{state},"limit":{limit}}

    headers = {
	    "X-RapidAPI-Key": get_key(),
	    "X-RapidAPI-Host": "realty-mole-property-api.p.rapidapi.com"
        }
    request_url = {'method':'GET', 'url':url, 'headers':headers,'params':querystring}
    return request_url

def api_request(url):
    try:
        response = requests.request(url["method"], url["url"], headers=url["headers"], params=url["params"])
        response.raise_for_status()
        # Code here will only run if the request is successful
        increase_request_counter()
        return response
    except requests.exceptions.HTTPError as errh:
        print(errh)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
    except requests.exceptions.Timeout as errt:
        print(errt)
    except requests.exceptions.RequestException as err:
        print(err)

def save_data(response):
    with open('sample.json', "wb") as file:
        file.write(response)

def load_comps():
    with open('sample.json','r') as file:
        data = json.load(file) 
    return data

def main(option):
    """ 
        Does: xxx
        Arguments explanation: xxx
        Return: xxx
    """
    if option == 'save':
        url = create_url("salePrice", "5500 Grand Lake Dr", "San Antonio", "TX", 78244)
        response = api_request(url)
        save_data(response.content)
        df_realty_comps = pd.DataFrame(response.json()['listings'])
    elif option == 'load':
        data = load_comps()
        df_realty_comps = pd.DataFrame(data['listings'])
        print(df_realty_comps)
    
    

if __name__ == "__main__":
    main('load')