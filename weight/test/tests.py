import requests , json
import os


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



def test_weightPost_route( path, expected, testname = 0):
    global url
    global status
    res =''
    expected_res = str(expected)
    try:
        res = requests.post(url + path)
        res = str(res.content.decode('utf-8'))
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print (message)
        status = 1

    if not expected_res in res:
        print(expected_res)
        print(res)
        print('test name: {}'.format(testname))
        status = 1

def test_batch_weight(path, expected , testname = 0):
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
        print('test name: {}'.format(testname))
        print(str(type(res))+ " "+ str(res))
        print(str(type(expected_res))+ " "+ str(expected_res))
        status = 1

def test_health():
    global url
    global status
    global test

    if test:
        url = 'http://18.194.232.207:8088'
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
        res = json.dumps(res.json())
        expected_res = json.dumps(expected)
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print (message)
        status = 1

    if res != expected_res:
        status = 1


test = False
def main():
    test_health()
    test_get_routes('/unknown' ,{"7":{"ContainerID":"C1","Produce":"Test","TransactionID":"36"}})
    test_get_routes('/item/Truck1?from=20200202112732&to=20211231011500' ,{"id":"Truck1","sessions":[35],"tara":92})
    test_get_routes('/session/35' , {"id": "35","truckID": "Truck1","items": [{"produce": "Oranges", "bruto" : "46", "neto": "null"},{"produce": "Apples", "bruto" : "76", "neto": "null"}]})


    test_weightPost_route("/weight?direction=in&truck=DebugTruck&containers=C1%3APeaches%2BC1%3APeaches%2BC2%3ABananas&weight=390",'')
    test_weightPost_route("/weight?direction=none&truck=DebugTruck&containers=C1%3APeaches%2BC2%3ABananas&weight=308",'{"37":{"bruto":"390","truck":"DebugTruck"}}' , 1)
    test_weightPost_route("/weight?direction=none&truck=DebugTruck&containers=C2%3ABananas&weight=236",'{"37":{"bruto":"390","truck":"DebugTruck"}}' , 2)
    test_weightPost_route("/weight?direction=out&truck=DebugTruck&containers=&weight=150",'{"37":{"bruto":"390","neto":"210","truck":"DebugTruck","truckTara":"150"}}',3 )

    test_batch_weight("/batch-weight", "file not found or it already in database" , 4)

    print(status)

main()