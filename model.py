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
import plotly.figure_factory as ff
import plotly.graph_objs as go

# data manipulation
import pandas as pd
import json
import math
import numpy as np

# dotenv handling
from api_key import get_key
from api_key import increase_request_counter

#others
from datetime import datetime


def create_url(endpoint, full_address):
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

    address = full_address['address']
    city = full_address['city']
    state = full_address['state']
    zipcode = full_address['zipcode']
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

def get_api_data(address):
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
    endpoints = ['properties', 'salePrice']
    for endpoint in endpoints:
        url = create_url(endpoint, address)
        response = api_request(url)
        if endpoint == 'properties':
            temp = json.loads(response.text)
            data[endpoint] = temp[0]
        else:
            data[endpoint] = json.loads(response.text)
             
        data['last_request'] = {'date_time':str(datetime.now())}
        save_data(data, 'home.json')
    return data

def get_data(address):
    """
        Does: retrieves the data from the api or the local drive\n
        Arguments: address dictionary\n
        Returns: json object\n
    """
    
    if len(address['address']) == 0:
        data = load_local_data('home.json')     
    else:
        data = get_api_data(address)
    return data

def process_data(address):
    """
        does: split and organize data. \n
        returns: house_df, sale_df, taxes_df, house_features, house_owner, last_request\n
    """
    data = get_data(address)

    tax_assessment_df = pd.DataFrame()
    taxes_df = pd.DataFrame()
    house_features = {}
    house_owner = {}
    property_data = {}
    property_comps = {}

    if "properties" in data:
        last_request = data['last_request']['date_time']
        property_data = data['properties']

    if "salePrice" in data:
        property_comps = data['salePrice']

    if 'features' in property_data:
        house_features = property_data['features'] # return this
        property_data.pop('features')

    if 'taxAssessment' in property_data:
        tax_assessment_df = pd.DataFrame.from_dict(property_data['taxAssessment'],orient='index')  # return this
        tax_assessment_df.reset_index(inplace=True)
        tax_assessment_df['total'] = tax_assessment_df.sum(axis=1)
        tax_assessment_df['total']= tax_assessment_df['total'].apply(lambda x: "${:,.2f}".format(x))
        tax_assessment_df.rename(columns = {'index':'year'},inplace=True)
        property_data.pop('taxAssessment')

    if 'propertyTaxes' in property_data:
        taxes_df = pd.DataFrame.from_dict(property_data['propertyTaxes'],orient='index')  # return this
        taxes_df.reset_index(inplace=True)
        taxes_df.rename(columns = {'index':'year','total':'taxes'},inplace=True)
        taxes_df['taxes']= taxes_df['taxes'].apply(lambda x: "${:,.2f}".format(x))
        taxes_df['assessment'] = tax_assessment_df['total']
        property_data.pop('propertyTaxes')

    if 'owner' in property_data:
        house_owner = property_data['owner'] # return this
        property_data.pop('owner')

    house_df = pd.DataFrame() # return this
    sale_df = pd.DataFrame() # return this

    if len(property_comps) > 0:
        for i in range(3):
            property_data[(list(property_comps)[i])] = property_comps[(list(property_comps)[i])]
        sale_df = pd.DataFrame.from_dict(property_comps['listings'])
        sale_df.drop('id', axis=1, inplace=True)
        sale_df.fillna('',inplace=True)
        sale_df['price']= sale_df['price'].apply(lambda x: "${:,.2f}".format(x))
        sale_df['distance']= sale_df['distance'].apply(lambda x: round(x, 2))
        
        
    for items in property_data.keys():
        house_df[items] = [property_data[items]]

    return house_df, sale_df, taxes_df, house_features, house_owner, last_request

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


def map_plot_property(df):
    """ 
        Does: generates a map with the location of the propety\n
        Arguments: \n
            df: dataframe with house data\n
    """
    fig = px.scatter_mapbox(df,
                        lat="latitude",
                        lon="longitude",
                        color_continuous_scale=px.colors.cyclical.IceFire, 
                        size="squareFootage",
                        size_max=30,
                        zoom=15,
                        hover_name="addressLine1")
    fig.update_layout(mapbox_style="open-street-map")
    return fig

def load_states():
    """
        does: read a html file with that has the USA states and the abbreviations for them\n
        return: dataframe with all the states and abbreviations\n
    """
    tables = pd.read_html('states.html')
    df = tables[0]
    print(len(df))

    df1 = df.iloc[:,[0,1,2]]
    df1.drop('FIPS Code', axis=1, inplace=True)
    df1.rename(columns = {'State':'state','Postal Abbr.':'abbr'},inplace=True)

    df2 = df.iloc[:,[3,4,5]]
    df2.drop('FIPS Code.1', axis=1, inplace=True)
    df2.rename(columns = {'State.1':'state','Postal Abbr..1':'abbr'},inplace=True)


    frames = [df1, df2]
    df_fix = pd.concat(frames)
    df_fix.reset_index(drop=True, inplace=True)
    df_fix.dropna(inplace=True)
    states = list(df_fix['abbr'])
    return states

def plot_tables(df):
    """
        does: create table from a given dataframe\n
        return: the table in a plotly fig object\n 
    """
    fig =  ff.create_table(df)
    return fig

def scatter_plot(df, x_column, y_column):
    """
        does: create scatter plot from a given dataframe\n
        return: the table in a plotly express fig object\n 
    """
    df['price'] = df['price'].apply(lambda x: x.replace(',', '').replace('$', ''))
    df['lotSize'] = df['lotSize'].replace('', np.nan, regex=True)
    fig = px.scatter(df, x = x_column, y = y_column,
                    color="address", hover_data=["correlation","distance","bedrooms","bathrooms","propertyType","squareFootage","lotSize"],height=400,width=600)
    return(fig)

def main():
    """ 
        Does: only for testing purpose
        Arguments: 
            Option: load or save
    """

if __name__ == "__main__":
    main()