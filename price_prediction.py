import pandas as pd # data processing
import numpy as np # working with arrays

import plotly_express as px
import matplotlib.pyplot as plt

from plotly.subplots import make_subplots
import plotly.graph_objects as go

import seaborn as sns # visualization
from termcolor import colored as cl # text customization

from sklearn.model_selection import train_test_split # data split

from sklearn.linear_model import LinearRegression # OLS algorithm
from sklearn.linear_model import Ridge # Ridge algorithm
from sklearn.linear_model import Lasso # Lasso algorithm
from sklearn.linear_model import BayesianRidge # Bayesian algorithm
from sklearn.linear_model import ElasticNet # ElasticNet algorithm

from sklearn.metrics import explained_variance_score as evs # evaluation metric
from sklearn.metrics import r2_score as r2 # evaluation metric

from model import process_data
from model import map_plot_property

def relational_plots(df):
    fig, axes = plt.subplots(3, 2, figsize=(10, 10))
    fig.suptitle('Price Relation')
    sns.scatterplot(ax=axes[0, 0], data = df, x ="squareFootage", y ="price", hue ="formattedAddress", legend = False, edgecolor = 'b')
    sns.scatterplot(ax=axes[0, 1], data = df, x ="distance", y ="price", hue ="formattedAddress", legend = False, edgecolor = 'b')
    sns.scatterplot(ax=axes[1, 0], data = df, x ="bedrooms", y ="price", hue ="formattedAddress", legend = False, edgecolor = 'b')
    sns.scatterplot(ax=axes[1, 1], data = df, x ="bathrooms", y ="price", hue ="formattedAddress", legend = False, edgecolor = 'b')
    sns.scatterplot(ax=axes[2, 0], data = df, x ="lotSize", y ="price", hue ="formattedAddress", legend = False, edgecolor = 'b')
    sns.scatterplot(ax=axes[2, 1], data = df, x ="yearBuilt", y ="price", hue ="formattedAddress", legend = False, edgecolor = 'b')
    return(plt)

def Distribution_plot(df):
    sns.histplot(df['price'], color = 'r', kde=True)
    plt.title('Sale Price Distribution', fontsize = 16)
    plt.xlabel('Sale Price', fontsize = 14)
    plt.ylabel('Frequency', fontsize = 14)
    plt.xticks(fontsize = 12)
    plt.yticks(fontsize = 12)

    plt.savefig('distplot.png')
    plt.show()

def data_split(df):
    X_var = df[['bedrooms', 'bathrooms', 'squareFootage', 'lotSize']].values
    y_var = df['price'].values

    X_train, X_test, y_train, y_test = train_test_split(X_var, y_var, test_size = 0.2, random_state = 0)
    return X_train, X_test, y_train, y_test

def modeling():
    X_train, X_test, y_train, y_test = data_split(comps_df)

    # 1. OLS

    ols = LinearRegression()
    ols.fit(X_train, y_train)
    ols_yhat = ols.predict(X_test)

    # 2. Ridge

    ridge = Ridge(alpha = 0.5)
    ridge.fit(X_train, y_train)
    ridge_yhat = ridge.predict(X_test)

    # 3. Lasso

    lasso = Lasso(alpha = 0.01)
    lasso.fit(X_train, y_train)
    lasso_yhat = lasso.predict(X_test)

    # 4. Bayesian

    bayesian = BayesianRidge()
    bayesian.fit(X_train, y_train)
    bayesian_yhat = bayesian.predict(X_test)

    # 5. ElasticNet

    en = ElasticNet(alpha = 0.01)
    en.fit(X_train, y_train)
    en_yhat = en.predict(X_test)

def multiplot(df):
    fig1 = px.scatter(df, x='squareFootage', y='price',
                    color="formattedAddress", size='price',
                    hover_name="price",
                    hover_data=["address", "propertyType", "bedrooms", "bathrooms", "squareFootage", "correlation", "price", "distance", "daysOld"]
                    )
    fig2 = px.scatter(df, x='distance', y='price',
                    color="formattedAddress", size='price',
                    hover_name="address",
                    hover_data=["propertyType", "bedrooms", "bathrooms", "squareFootage", "correlation", "price", "distance", "daysOld"]
                    )
    fig3 = px.scatter(df, x='bedrooms', y='price',
                    color="formattedAddress", size='price',
                    hover_name="address",
                    hover_data=["propertyType", "bedrooms", "bathrooms", "squareFootage", "correlation", "price", "distance", "daysOld"]
                    )
    fig4 = px.scatter(df, x='bathrooms', y='price',
                    color="formattedAddress", size='price',
                    hover_name="address",
                    hover_data=["propertyType", "bedrooms", "bathrooms", "squareFootage", "correlation", "price", "distance", "daysOld"]
                    )
    fig5 = px.scatter(df, x='lotSize', y='price',
                    color="formattedAddress", size='price',
                    hover_name="address",
                    hover_data=["propertyType", "bedrooms", "bathrooms", "squareFootage", "correlation", "price", "distance", "daysOld"]
                    )
    fig6 = px.scatter(df, x='yearBuilt', y='price',
                    color="formattedAddress", size='price',
                    hover_name="address",
                    hover_data=["propertyType", "bedrooms", "bathrooms", "squareFootage", "correlation", "price", "distance", "daysOld"]
                    )

    fig = make_subplots(
    rows=3, cols=2,
    subplot_titles=("Relation SquareFootage/Price","Relation Distance/Price", 
                    "Relation Bedrooms/Price", "Relation Bathrooms/Price", 
                    "Relation Lot Size/Price", "Relation Year of Built/Price"),
    shared_xaxes=False)
    fig.append_trace(fig1, row=1,col=2)
    fig.append_trace(fig2,row=1,col=2)
    fig.append_trace(fig3,row=2,col=1)
    fig.append_trace(fig4,row=2,col=2)
    fig.append_trace(fig5,row=3,col=1)   
    fig.append_trace(fig6,row=3,col=2)   
    fig.update_layout(showlegend=False, title_text="Specs with Subplot Title")
    fig.show()


def main():
    sns.set_style('whitegrid') # plot style

    address = {} #transform the address to the correct format

    house_df, sale_df, tax_assessment_df, taxes_df, house_features, house_owner, last_request = process_data(address)

    relational_plots(sale_df).show()
    #Distribution_plot(sale_df)
    #multiplot(sale_df)


if __name__ == '__main__':
    main()