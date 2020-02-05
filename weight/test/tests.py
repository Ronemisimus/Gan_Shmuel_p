import requests , json
import os
from datetime import datetime



status = 0
url = "http://localhost:{}".format(os.environ['PORT'])


def test_health():
    global url
    global status
    try:
        requests.get(url + '/health')
    except Exception as e :
        status = 1

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


def test_unknown(path , expected):
    global url
    global status
    res = ''
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

def main():
    
    #testing session  route
    test_weight_route('/session/35' ,{"id": "35","truckID": "Truck1","items": [{"produce": "Oranges", "bruto" : "46", "neto": "null"},{"produce": "Apples", "bruto" : "76", "neto": "null"}]} )

    # testing item route
    test_item_route('/item/truck1' ,{"id":"truck1","sessions":[35],"tara":92})
    
    # #Testing Inserting Transaction with 3 containers using POST /weight
    # timeIn=datetime.now().strftime("%Y%m%d%H%M%S")
    # test_weightPost_route("/weight?direction=in&truck=DebugTruck&containers=C1%3APeaches%2BC1%3APeaches%2BC2%3ABananas&weight=390","<Response [200]>")
    # test_weightPost_route("/weight?direction=none&truck=DebugTruck&containers=C1%3APeaches%2BC2%3ABananas&weight=308","<Response [200]>")
    # test_weightPost_route("/weight?direction=none&truck=DebugTruck&containers=C2%3ABananas&weight=236","<Response [200]>")
    # test_weightPost_route("/weight?direction=out&truck=DebugTruck&containers=&weight=150","<Response [200]>")
    # timeOut=datetime.now().strftime("%Y%m%d%H%M%S")

    # # # Testing if Transaction was entered successfully
    # test_weightafterPost_route("/weight?from=%s&to=%s&filter=out"%(str(timeIn),str(timeOut)),'{"bruto":"390","containers":"C1,C2","direction":"Out","neto":"210","produces":"Bananas,Peaches"}')


    # #testing /health route
    test_health()
    test_batch_weight("/batch-weight", "file not found or it already in database")

    # testing /unknown route
    test_unknown("/unknown",{"7":{"ContainerID":"C1","Produce":"Test","TransactionID":"36"},"8":{"ContainerID":"C1","Produce":"Bananas","TransactionID":"37"},"9":{"ContainerID":"C2","Produce":"Peaches","TransactionID":"37"}})
    print(status)

main()
