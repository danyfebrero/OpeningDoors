#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 23:22:00 2022

@author: Daniel Jimenez
"""
# API post/get
from datetime import datetime
import requests

# plotting
import plotly.express as px

# data manipulation
import json

# dotenv handling
from api_key import get_key
from api_key import increase_request_counter

#others
from datetime import datetime


def create_url(endpoint, address, city, state, zipcode, squareFootage=None, 
                bathrooms=None, bedrooms=None, propertyType=None, compCount=None, limit=None):
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
    headers = {
	    "X-RapidAPI-Key": get_key(),
	    "X-RapidAPI-Host": "realty-mole-property-api.p.rapidapi.com"
        }
    if endpoint == 'properties':
        querystring = {'address':f'{address}, {city}, {state}, {zipcode}'}
    elif endpoint == 'salePrice' or endpoint == 'rentalPrice':
        querystring = {'address':f'{address}, {city}, {state}, {zipcode}'}
    elif endpoint == 'saleListings' or endpoint == 'rentalListings':
        querystring = {'city':{city},'state':{state}}

    request_url = {'method':'GET', 'url':url, 'headers':headers,'params':querystring}

    return request_url

def api_request(url):
    """ 
        Does: does de request to the API \n
        Arguments: url is a list\n
        Return: the response or the error\n
    """
    try:
        response = requests.request(url["method"], url["url"], headers=url["headers"], params=url["params"])
        response.raise_for_status()
        increase_request_counter()
    except requests.exceptions.HTTPError as errh:
        return errh
    except requests.exceptions.ConnectionError as errc:
        return errh
    except requests.exceptions.Timeout as errt:
        return errh
    except requests.exceptions.RequestException as err:
        return errh
    return response

def save_data(data, filename):
    """ 
        Does: save all the data obtained from the API to a json file\n
        Arguments: \n
            data: is the list of dictionaries obtained from the API\n
            filename: the name and extension to export the file\n
    """
    with open(filename, "w") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def load_local_data(filename):
    """ 
        Does: loads the data saved from the API to a json file\n
        Arguments: \n
            filename: the name and extension to of the file to load\n
        Returns: a the dictionaries obtained from the file\n
    """
    with open(filename,'r') as file:
        data = json.load(file) 
    return data

def get_api_data(address, endpoints):
    """ 
        Does: gets all the data from the api\n
        Arguments: 
            address = {"address" : "string", "city" : "string", "state" : "string", "zipcode" : integer}\n
            endpoints = a list of the endpoits needed\n
            Available Endpoints: 'properties', 'salePrice', 'rentalPrice', 'saleListings','rentalListings'\n       
        Returns: all the data obtained from the api in a dictionary with the same name as the endpoint
    """
    data = {}
    
    for endpoint in endpoints:
        url = create_url(endpoint, address['address'], address['city'], address['state'], address['zipcode'])
        response = api_request(url)
        if not endpoint == 'properties':
            data[endpoint] = json.loads(response.text)
        else:
             temp = json.loads(response.text)
             data[endpoint] = temp[0]
        data['last_request'] = {'date_time':str(datetime.now())}
        save_data(data, 'home.json')
    return data
