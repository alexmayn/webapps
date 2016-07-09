********************************************************************
*********** Blog for studing web-technologies of Python ************
********************************************************************

Blog on Python with Flask, MongoDB.
It contain autorization, administration and logging functions.

For starting project you must be using wsgi.py
For docker start you should use this command:

             $ docker pull maynagashev/webapp

   Structure of project:


                        wsgi.py   - wrapper for start project

                        config.py - all config constants
                        admin.py  - classes and views for administration
                        auth.py   - function for check user for admin rights

                        populateDB.py - add users to DB


                        ex - directory of main modules/ It contein:
                             __init__  - initializer module
                             forms.py  - login form
                             models.py - classes description
                             user.py   - user class description
                             views.py  - main functions of showing views & some classes for showing articles

