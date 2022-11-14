# OpeningDoors

Get your home’s value and see selling options. 
This is my Final Project for Code Louisville Data Analytics 2.

## GitHub repository
https://github.com/danyfebrero/OpeningDoors

## Project Brief

This project will allow the user to search a home value, and analyze selling and rental options.

## Requirements:
  * Python 3.9
  * python-dotenv
  * requests
  * plotly_express
  * Pandas
  * Realty Mole Property API key (gives 50 Requests per month in the free suscription) at https://www.realtymole.com/api
  * Numpy
  * Matplotlib
  * Seaborn
  * Sklearn

We recommend Python 3.9.7 or higher. If you don't have Python installed, please follow the download instructions on the official website https://www.python.org 

Once you have Python installed follow hte next steps to create a virtual enviroment and install the Python libraries, using your command line interface type: 
 * Create a virtual enviroment 

       python3 -m venv venv
       
       source ./venv/bin/activate
 
 * installing packages

       pip instal -r requirements.txt

## How to run the project
### For mac and linux:
 * Location of module containing the app:

        export FLASK_APP=openingdoors.py

* Enable developers features like debugging:
    
        export FLASK_ENV=development

* Run the application:
    
        flask run

### For windows:
* Location of module containing the app:
        
        set FLASK_APP=openingdoors.py

* Enable developers features like debugging:
        
        set FLASK_ENV=development

* Run the application:
    
        flask run

## How to quit the project:

        press control + c in the command line
        
## Features:

  ### Read TWO datasets from an API
  This project will first ingest a dataset from the Realty Mole Property API when searching for an address based on input provided by the user.
  * Property Records
  * Valuation Estimates
  * Comparable Listings
  ### Clean your data and perform a pandas merge with your two data sets, then calculate some new values based on the new data set
  Description
  ### Make 3 matplotlib or seaborn (or another plotting library) visualizations to display your data
  Description
  ### Utilize a virtual environment and include instructions in your README on how the user should set one up
  The project will include a requirements.txt file, allowing the user to install all dependencies using the dependency management tool of their choice. Instructions will be included for using venv to setup the project.
  
