#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 16:12:16 2022

@author: Daniel Jimenez
"""

import os
import subprocess

from os.path import exists
from os import path

subprocess.call(["clear"])

def key_exist():
    """
        Does: check if the file exist and is not empty
    """
    return exists ("creds.py") and path.getsize("creds.py") != 0

def create_key(key_input):
    with open("creds.py","w") as file:
        key =f"API_KEY = {key_input}"
        file.write(key)

def get_key():
    """ 
        Does: if the key is saved loads the key if not then ask for one
        Return: the key from the file or the new one
    """
    pass

if __name__ == "__main__":
    get_key()