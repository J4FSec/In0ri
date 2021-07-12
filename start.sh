#!/bin/bash

exec service cron start &
exec /usr/bin/python3 /opt/In0ri/FlaskApp/app.py &
exec /usr/bin/python3 /opt/In0ri/api.py