import requests
import os
from datetime import datetime


def validate(status, content):
    log_info = ""
    if status >= 500 or status <= 599 :
        log_info = "Status:  {}\n Content:\n{} \n Fail.\n".format(status, content)
        print("1")
    else:
        log_info = "Status:  {}\n Content:\n{} \nInvalid url \n".format(status, content)
        print("0")
    return log_info


url = "http://localhost:{}".format(os.environ['PORT'])

valid_data = ""
res = requests.get( url + valid_data )
log = validate(res.status_code, res.content)
with open("log.log", 'a+') as f:
    f.write("\n\n" + str(datetime.now()) + "\n\n")
    f.write("\nRoute:\t" + route + "\nValidation Data: \t" + item + "\n" + log + "\n")
