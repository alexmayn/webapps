********************************************************************
*********** Blog for studing web-technologies of Python ************
********************************************************************

Blog on Python with Flask, MongoDB.
It contain autorization, administration and logging functions.

For starting project you must be using wsgi.py
For docker start you should use this command:

            $ docker pull maynagashev/webapp
And Run docker with volume sharing

            $ sudo docker run -v /home/administrator/docker/flask:/home/flask --dns YOURE_DNS -p 127.0.0.1:222:22 -p 127.0.0.1:8080:80 -i -t baseimage-ex.com-flask-tb3 /sbin/my_init -- bash -l

Add host to hosts

            $ vim /etc/hosts
            
Next line:
127.0.0.1     ex.com


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

