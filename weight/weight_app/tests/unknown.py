

#TEST /unknown route

import requests
from datetime import datetime

def write_log():
    global log
    
    with open("log.log", 'a+') as f:
        f.write(log)
    

def success_log():
    global log
    log = now_time + " /unknown : status code 200 - OK\n"

def fail_log():
    global log
    log = log = now_time + " /unknown : Error! status code is not 200 - OK\n"
    
res = requests.get('http://localhost:8088/unknown')

now = datetime.now()
now_time = now.strftime("%d/%m/%Y %H:%M:%S")

if (res.status_code == 200):
    success_log()
else:
    fail_log()
write_log()



