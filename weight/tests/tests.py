
#POST /weight
#  Return value on success is:
#  { "id": <str>, 
#    "truck": <license> or "na",
#    "bruto": <int>,
#    ONLY for OUT:
#    "truckTara": <int>,
#    "neto": <int> or "na" // na if some of containers have unknown tara
#  }

# POST /batch-weight
#  - file=<filename>

# GET /unknown   Returns a list of all recorded containers that have unknown weight: ["id1","id2",...]

# GET /weight?from=t1&to=t2&filter=f
# - t1,t2 - date-time stamps, formatted as yyyymmddhhmmss. server time is assumed.
# - f - comma delimited list of directions. default is "in,out,none"
# default t1 is "today at 000000". default t2 is "now". 
# returns an array of json objects, one per weighing (batch NOT included):
# [{ "id": <id>,
#    "direction": in/out/none,
#    "bruto": <int>, //in kg
#    "neto": <int> or "na" // na if some of containers have unknown tara
#    "produce": <str>,
#    "containers": [ id1, id2, ...]
# },...]

# GET /item/<id>?from=t1&to=t2
# - id is for an item (truck or container). 404 will be returned if non-existent
# - t1,t2 - date-time stamps, formatted as yyyymmddhhmmss. server time is assumed.
# default t1 is "1st of month at 000000". default t2 is "now". 
# Returns a json:
# { "id": <str>,
#   "tara": <int> OR "na", // for a truck this is the "last known tara"
#   "sessions": [ <id1>,...] 
# }


# GET /session/<id>
# - id is for a weighing session. 404 will be returned if non-existent
# Returns a json:
#  { "id": <str>, 
#    "truck": <truck-id> or "na",
#    "bruto": <int>,
#    ONLY for OUT:
#    "truckTara": <int>,
#    "neto": <int> or "na" // na if some of containers unknown
#  }

#  GET /health
#  - By default returns "OK" and status 200 OK
#  - If system depends on external resources (e.g. db), and they are not available (e.g. "select 1;" fails ) then it should return "Failure" and 500 Internal Server Error

import requests
import os
from datetime import datetime


def validate(status, content):
    log_info = ""
    if status == 200:
        log_info = "Status:  {}\n Content:\n{} \nYeah ;) \n".format(status, content)
        validate_response(content)
        print("0")
    elif status == 404:
        log_info = "Status:  {}\n Content:\n{} \nInvalid url \n".format(status, content)
        print("0")
    else:
        log_info = "Status:  {}\n Content:\n{} \n Fail.\n".format(status, content)
        print("1")
    return log_info


def validate_response(content){
    #check if content is valid json file

    print("0")
}

url = "http://localhost:{}".format(os.environ['PORT'])
# url ="http://18.194.232.207:{}".format(os.environ['PORT'])


#add date to log file
with open("log.log", 'a+') as f:
    f.write("\n\n" + str(datetime.now()) + "\n\n")

get_routes  = [ "/" , "/health" , "/weight", "/batch-weight", "/unknown", "/item" , "/session" ]


post_routes = [ "/weight", "/batch-weight" ]
validations = {"/":[""], "/health" : [""], "/weight": ["from=t1&to=t2&filter=f", "?from=aaa&to=bbb"]}

for route, test in validations.items():
    for item in test:
        res = requests.get( url + route + item )
        log = validate(res.status_code, res.content)
        with open("log.log", 'a+') as f:
            f.write("\nRoute:\t" + route + "\nValidation Data: \t" + item + "\n" + log + "\n")

print ("0")