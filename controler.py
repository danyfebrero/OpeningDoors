#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 23:22:00 2022

@author: Daniel Jimenez
"""
# data handling
import pandas as pd
# plotting
import plotly.express as px

from model import get_api_data
from model import load_local_data


def map_plot(df, street):
    """ 
        Does: generates a map with the locations of the comparables\n
        Arguments: \n
            df: dataframe with the listing of the comparables\n
            street: address of the house\n
    """
    fig = px.scatter_mapbox(df, 
                        lat="latitude", 
                        lon="longitude",     
                        color="address", 
                        color_continuous_scale=px.colors.cyclical.IceFire, 
                        size="correlation",
                        size_max=30, 
                        zoom=15,
                        hover_name="address",
                        hover_data=["propertyType", "bedrooms", "bathrooms", "squareFootage", "correlation", "price", "distance", "daysOld"],
                        title="Comparables for {0}".format(street))
    fig.update_layout(mapbox_style="open-street-map")                    
    #fig.show()
    return fig

def scatter_plot(df, street):
    """ 
        Does: generates a scatter plot with the price square feet relation of the comparables\n
        Arguments: \n
            df: dataframe with the listing of the comparables\n
            street: address of the house\n
    """
    fig = px.scatter(df,
                    x='squareFootage',
                    y='price',
                    hover_name="address",
                    hover_data=["propertyType", "bedrooms", "bathrooms", "squareFootage", "correlation", "price", "distance", "daysOld"],
                    title="Comparables for {0}".format(street))
    #fig.show()
    return(fig)

def check_data_content(data):
    # leer los 3 difertentes diccionarios
    # verificar el contenido del dicionario
    # separar los  listings en los dos ultimos diccionarios
    # devolver los 3 diccionarios y dos dataframes con los listing de venta y renta
    return True

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
    elif location == 'local':
        data = load_local_data('home.json')
    #street = data['properties']['formattedAddress']
    #df_sale_comps = pd.DataFrame(data['salePrice']['listings'])
    #df_rent_comps = pd.DataFrame(data['rentalPrice']['listings'])
    #map_plot(df_sale_comps, street)
    #scatter_plot(df_sale_comps, street)
    #df = pd.DataFrame(data)
    #print(data)
    return data


def main():
    """ 
        Does: only for testing purpose
        Arguments: 
            Option: load or save
    """
    endpoints = []
    address = {}
    location = 'local'
    get_data(location, address, endpoints)
    
    
if __name__ == "__main__":
    main()

