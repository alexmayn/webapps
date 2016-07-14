#!/usr/bin/python

from werkzeug.security import generate_password_hash
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


def main():
    # Connect to the DB
    collection = MongoClient()["ex_site"]["user"]

    # Create interactive user
    user = unicode(raw_input("Enter your username: "))
    isadmin = raw_input("Is administrator? (True or False): ")
    password = ''
    while len(password)<10:
        password = raw_input("Enter your password: ")
        if len(password)<10:
            print("Your password is too short, please retype it longer.")

    address  = raw_input("Your address: ")
    firstname = raw_input("First name: ")
    secondname = raw_input("Second name: ")
    email = raw_input("e-mail: ")


    pass_hash = generate_password_hash(password, method='pbkdf2:sha256')

    # Insert the user in the DB
    try:
        collection.insert({"_id": user,
                           #"_cls": 'User', #-- comment it For superuser, user not view at list and do not removing by default function in admin console
                                            # for view in admin console uncomment it
                           "login": user,
                           "password": pass_hash,
                           "isadmin": isadmin,
                           "address": address,
                           "firstname": firstname,
                           "secondname": secondname,
                           "email": email
                           })
        print "User created."
    except DuplicateKeyError:
        print "User already present in DB."


if __name__ == '__main__':
    main()
