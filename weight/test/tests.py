import requests , json
import os
from datetime import datetime



status = 0
url = "http://localhost:{}".format(os.environ['PORT'])





def test_weight_route( path, expected):
    global url
    global status
    res =''
    expected_res = ''
    try:
        res = requests.get(url + path)
        res = json.dumps(res.json())
        expected_res = json.dumps(expected)
    except Exception as e:
        status = 1

    if res != expected_res:
        status = 1



		
def test_item_route( path, expected):
    global url
    global status
    res =''
    expected_res = ''
    try:
        res = requests.get(url + path)
        res = json.dumps(res.json())
        expected_res = json.dumps(expected)
    except Exception as e:
        status = 1

    if res != expected_res:
        status = 1

def test_weightPost_route( path, expected):
    global url
    global status
    res =''
    expected_res = ''
    try:
        res = str(requests.post(url + path))
        expected_res = expected
    except Exception as e:
        status = 1

    if res != expected_res:
        status = 1

def test_weightafterPost_route( path, expected):
    global url
    global status
    res =''
    expected_res = expected
    try:
        res = str(requests.get(url + path).content)
    except Exception as e:
        status = 1
    if not expected_res in res:
        status = 1

def test_batch_weight(path, expected):
    global url
    global status
    res =''
    expected_res = ''
    try:
        res = requests.post(url + path, data = {"filename" : ""})
        res = res.content.decode('utf-8')
        expected_res=expected
    except Exception as e:
        status = 1

    if res != expected_res:
        status = 1

def test_health():
    global url
    global status
    try:
        requests.get(url + '/health')
    except Exception as e :
        status = 1

def test_get_routes(path , expected):
     
    global url
    global status
    global test

    if test:
        url = 'http://18.194.232.207:8088'
    
    res = ''
    expected_res = ''

    try:
        res = requests.get(url + path)
        print
        res = json.dumps(res.json())
        expected_res = json.dumps(expected)
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print (message)
        status = 1

    if res != expected_res:
        print(res)
        print(expected_res)
        status = 1


test = False
def main():
    test_health()


    test_get_routes('/unknown' ,{"7":{"ContainerID":"C1","Produce":"Test","TransactionID":"36"}})
    test_get_routes('/item/Truck1?from=20200202112732&to=20211231011500' ,{"id":"Truck1","sessions":[35],"tara":92})
    test_get_routes('/session/35' , {"id": "35","truckID": "Truck1","items": [{"produce": "Oranges", "bruto" : "46", "neto": "null"},{"produce": "Apples", "bruto" : "76", "neto": "null"}]})
    print(status)

main()
