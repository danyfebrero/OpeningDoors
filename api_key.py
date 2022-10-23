#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 16:12:16 2022

@author: Daniel Jimenez
"""

import os
from os.path import exists
from os import path
from dotenv import load_dotenv
from dotenv import dotenv_values


def configure():
    load_dotenv()

def key_exist():
    """
        Does: check if the file exist and is not empty
    """
    return exists (".env") and path.getsize(".env") != 0

def create_key(key_input):
    """ 
        Does: creates a file with the api key from the user input
    """
    with open(".env","w") as file:
        key =f"API_KEY={key_input}"
        file.write(key)

def get_key():
    """ 
        Does: if the key is saved loads the key if not then ask for one
        Return: the key from the file or the new one
    """

    while not key_exist():
        key_input = input("Please introduce your Realty Mole API key (if you don't have a key please create one for free at https://rapidapi.com/realtymole/api/realty-mole-property-api: ")
        if len(key_input) == 0:
            continue
        create_key(key_input)
    configure()
    return os.getenv('API_KEY')

if __name__ == "__main__":
    get_key()