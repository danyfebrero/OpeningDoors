# OpeningDoors

Get your home’s value and see selling options. 
This is my Final Project for Code Louisville Data Analytics 2.

## GitHub repository
https://github.com/danyfebrero/OpeningDoors

## Project Brief

This project will allow the user to search a home value, and analyze the comparables.

## Requirements:
  * python 3.9
  * python-dotenv
  * requests
  * flask
  * plotly_express
  * plotly
  * pandas
  * Realty Mole Property API key (gives 50 Requests per month in the free suscription) at https://www.realtymole.com/api
  * math
  * termcolor
  * lxml
  * json
  * numpy


We recommend Python 3.9.7 or higher. If you don't have Python installed, please follow the download instructions on the official website https://www.python.org 

Once you have Python installed follow hte next steps to create a virtual enviroment and install the Python libraries, using your command line interface type: 
 * Create a virtual enviroment 

       python3 -m venv venv
       
       source ./venv/bin/activate
 
 * installing packages

       pip instal -r requirements.txt

## How to run the project

* Type in the command line:
    
        python run.py


## How to quit the project:

        press control + c in the command line
        
## Features:

  ### Read TWO datasets from an API
  This project will first ingest a dataset from the Realty Mole Property API when searching for an address based on input provided by the user.
  * Property Records
  * Valuation Estimates
  * Comparable Listings
  ### Clean your data and perform a pandas merge with your two data sets, then calculate some new values based on the new data set
  * merge the data recived from 2 calls to the api in a json file located in the local data.
  * split the data into some dataframes and dictionaries based on the needs.
  * calculated the total of assessment and created a new column in the dataframe to store it.
  * changed some formats to correct display to the user
  ### Make 3 matplotlib or seaborn (or another plotting library) visualizations to display your data
  * Used plotly, plotly express to generate tables, maps, and charts
  ### Utilize a virtual environment and include instructions in your README on how the user should set one up
  The project will include a requirements.txt file, allowing the user to install all dependencies using the dependency management tool of their choice. Instructions will be included for using venv to setup the project.
  
