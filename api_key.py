#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 16:12:16 2022

@author: Daniel Jimenez
"""

# working with files
import os
from os.path import exists
from os import path
#working with dotenv
from dotenv import load_dotenv
from dotenv import set_key

def update_env():
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
    set_key('.env','API_KEY',key_input)
    set_key('.env','Request_Counter',0)
    update_env()

def get_request_counter():
    if key_exist():
        os.getenv('Request_Counter')

def reset_request_counter():
    if key_exist():
        set_key('.env','Request_Counter',0)
        update_env()

def increase_request_counter():
    if key_exist():
        counter = int(get_request_counter())
        counter += 1
        set_key('.env','Request_Counter',counter)
        update_env()

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
    update_env()
    return os.getenv('API_KEY')

if __name__ == "__main__":
    get_key()