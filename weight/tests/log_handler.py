from datetime import datetime
import sys , os
from flask import request
from flask import current_app

def write_log(msg):
    # get current time
    now = datetime.now()
    msg_time = now.strftime("%d/%m/%Y %H:%M:%S")
    msg += ' ' + msg_time

    with open("log.log" , 'a+') as log:
        log.write(msg)

def check_connection(route):
    with current_app.app_context():

        request.get('google.com')
    return True

    