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
import pandas as pd
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
    #refactor this code
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
    #refactor this code
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

def get_data(location, address, endpoints):
    """
        Does:
        Arguments:
        Returns:
    """
    if location == 'api':
        if len(address) == 0:
            address = {"address" : "5500 Grand Lake Dr", "city" : "San Antonio", "state" : "TX", "zipcode" : 78244}
        if len(endpoints) == 0:
            endpoints = ['properties', 'salePrice']
        data = get_api_data(address, endpoints)
    else:
        data = load_local_data('home.json')
    return data

def process_data(location, address, endpoints):
    """
        returns: last_request, property_data, property_comps, property_rent
    """
    data = get_data(location, address, endpoints)
    endpoints = []
    address = {}
    location = 'local'
    data = get_data(location, address, endpoints)

    endpoints = list(data.keys())
    last_request = ''
    property_data = {}
    property_comps = {}
    property_rent = {}

    if "properties" in endpoints:
        last_request = data['last_request']['date_time']
        property_data = data['properties']

    if "salePrice" in endpoints:
        property_comps = data['salePrice']
        #comps_df = pd.DataFrame.from_dict(property_comps['listings'])
        #comps_df.drop('id', axis=1, inplace=True)

    if "rentalPrice" in endpoints:
        property_rent = data['rentalPrice']
        #rent_df = pd.DataFrame.from_dict(property_rent['listings'])
        #rent_df.drop('id', axis=1, inplace=True)

    coordinates = {
                    'latitude' : [property_data['latitude']],
                    'longitude' : [property_data['longitude']],
                    'address' : [property_data['addressLine1']],
                    'squareFootage' : [property_data['squareFootage']]
                    }
    df_coordinates = pd.DataFrame.from_dict(coordinates)
    property_map = map_plot_property(df_coordinates)


    return last_request, property_data, property_comps, property_rent, property_map

def map_plot(df):
    """ 
        Does: generates a map with the locations of the comparables\n
        Arguments: \n
            df: dataframe with the listing of the comparables\n
    """
    fig = px.scatter_mapbox(df, 
                        lat="latitude", 
                        lon="longitude",     
                        color="address", 
                        color_continuous_scale=px.colors.cyclical.IceFire, 
                        size="squareFootage",
                        size_max=30, 
                        zoom=15,
                        hover_name="address",
                        hover_data=["propertyType", "bedrooms", "bathrooms", "squareFootage", "correlation", "price", "daysOld"]
                        )
    fig.update_layout(mapbox_style="open-street-map")                    
    return fig

def scatter_plot(df, field):
    """ 
        Does: generates a scatter plot with the price square feet relation of the comparables\n
        Arguments: \n
            df: dataframe with the listing of the comparables\n
            field: x value\n
    """
    fig = px.scatter(df,
                    x = field,
                    y='price',
                    hover_name="address",
                    hover_data=["propertyType", "bedrooms", "bathrooms", "squareFootage", "correlation", "price", "distance", "daysOld"]
                    )
    return(fig)

def map_plot_property(df):
    """ 
        Does: generates a map with the location of the propety\n
        Arguments: \n
            df: dataframe with the listing of the comparables\n
    """
    fig = px.scatter_mapbox(df, 
                        lat="latitude", 
                        lon="longitude",
                        color_continuous_scale=px.colors.cyclical.IceFire, 
                        size="squareFootage",
                        size_max=30, 
                        zoom=15,
                        hover_name="address")
    fig.update_layout(mapbox_style="open-street-map")                    
    return fig


def main():
    """ 
        Does: only for testing purpose
        Arguments: 
            Option: load or save
    """
    endpoints = []
    address = {}
    location = 'local'
    last_request, property_data, property_comps, property_rent, property_map = process_data(location, address, endpoints)

    if 'features' in property_data:
        features_df = pd.DataFrame.from_dict(property_data['features'])
        property_data.pop('features')

    if 'taxAssessment' in property_data:
        tax_assessment_df = pd.DataFrame.from_dict(property_data['taxAssessment'],orient='index')
        tax_assessment_df.reset_index(inplace=True)
        tax_assessment_df.rename(columns = {'index':'year'})
        property_data.pop('taxAssessment')

    if 'propertyTaxes' in property_data:
        taxes_df = pd.DataFrame.from_dict(property_data['propertyTaxes'],orient='index')
        taxes_df.reset_index(inplace=True)
        taxes_df.rename(columns = {'index':'year'})
        property_data.pop('propertyTaxes')

    if 'owner' in property_data:
        owner_dict = property_data['owner']
        property_data.pop('owner')

    home_df = pd.DataFrame()
    sale_df = pd.DataFrame()
    rent_df = pd.DataFrame()

    if len(property_comps) > 0:
        for i in range(3):
            property_data[(list(property_comps)[i])] = property_comps[(list(property_comps)[i])]
        sale_df = pd.DataFrame.from_dict(property_comps['listings'])
        sale_df.drop('id', axis=1, inplace=True)

    if len(property_rent) > 0:
        for i in range(3):
            property_data[(list(property_rent)[i])] = property_rent[(list(property_rent)[i])]
        rent_df = pd.DataFrame.from_dict(property_rent['listings'])
        rent_df.drop('id', axis=1, inplace=True)
        
    for items in property_data.keys():
        home_df[items] = [property_data[items]]
    

    
if __name__ == "__main__":
    main()