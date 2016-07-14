#!/bin/sh

service ssh start
service nginx start

/usr/bin/uwsgi --uid root --ini /etc/uwsgi/apps-available/ex.ini &

mongod --logpath /var/log/mongodb/mongo.log --dbpath /home/flask/mongo 
