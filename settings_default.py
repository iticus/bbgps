'''
Created on Jul 31, 2014

@author: ionut
'''
#Edit and save as settings.py

import logging

#General settings
LOG_LEVEL = logging.INFO
SECRET = 'bbgps'

#Tornado settings
DEBUG = True
PORT = 9001
TEMPLATE_PATH = 'templates'
STATIC_PATH = 'static'

#Database settings
DB_URI = "mongodb://127.0.0.1/"
DB_NAME = 'bbgps'