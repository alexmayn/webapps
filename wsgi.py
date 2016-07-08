# -*- coding: utf-8 -*-

################################################################################
#
#                       Mini blog - website on Pyton
#   author: Alexander Mainagashev
#   date: 07.07.2016
################################################################################
"""
   Run project command: - Wrapper for start Project from Python environment (python/bin/python)

             $ python wsgi.py

   For docker start you should use this command:

             $ docker pull maynagashev/webapp


"""
from ex import app


# set pathes
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_script import Manager, Server

manager = Manager(app) # init flask manager

# Set manager config for start the manager
manager.add_command("runserver", Server(
     use_debugger = True,                #use debugger
     use_reloader = True,                #reload when changing
     host = '0.0.0.0')                   #address
)

#Start manager
if __name__=="__main__":
    manager.run()
