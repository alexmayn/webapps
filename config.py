from pymongo import MongoClient

DEBUG_TB_INTERCEPT_REDIRECTS = False # disable redirect requests for debugger
CRSF_ENABLED                 = True  # enable CSRF heqder

SECRET_KEY = 'my-super-secret-key'   # secret key




WTF_CSRF_ENABLED = True # CSRF for WTForms
DEBUG = True            # Using debug
DOWNLOAD_FOLDER = '../download/'# Folder for files for download
LOG = 'download/sitelog.log'    # Log file path
"""

   WhatFor: Configure of MongoDB connection

"""
# Data base Name
DB_NAME = 'ex_site'


# Init DB client of pymongo
DATABASE = MongoClient()[DB_NAME]
# Set table names
POSTS_COLLECTION = DATABASE.posts
USERS_COLLECTION = DATABASE.users
SETTINGS_COLLECTION = DATABASE.settings #it's not used

# Options configure DB
MONGODB_DB    =  DB_NAME
#MONGODB_HOST  = '127.0.0.1'
#MONGODB_PORT  =  27017
MONGODB_USERNAME = 'user'
MONGODB_PASSWORD = 'password'

 
