import requests , json
import os
from datetime import datetime



# # This is the repo
# def validate(status, content, expected):
#     print(content)
#     print(expected)
#     code = 0
#     log_info = ""
#     if 500 <= status <= 599 :
#         log_info = "Status:  {}\n Content:\n{} \n Fail.\n".format(status, content)
#         code = 1 
#     else:
#         if expected in content:
#             log_info = "Status:  {}\n Content:\n{} \n \n".format(status, content)
#         else:
#             log_info = "Status:  {}\n Invalid Content:\n{}\n Expected: \n{} \n respone not as expected.\n".format(status, content, expected)
#             code = 1
#     return log_info , code



# # Test Get request
# def test__get_routes(route, expected):
#     res = requests.get(route)
#     log , code  = validate(int(res.status_code), str(res.content), expected)
#     if code == 1:
#         print(log)


# # Test Post request
# def test__post_routes(route, expected):
#     res = requests.post(route)
#     log , code  = validate(int(res.status_code), str(res.content), expected)
#     if code == 1:
#         print(log)


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
    expected_res = ''
    try:
        print("made it to getweight1")
        res = str(requests.get(url + path))
        print("made it to getweight2")
        expected_res = expected
        print("made it to getweight3")
    except Exception as e:
        status = 1

    if expected_res in res:
        print("not equal!")
        status = 1

    
def main():
    
    #testing session  route
    test_weight_route('/session/35' ,{"id": "35","truckID": "Truck1","items": [{"produce": "Oranges", "bruto" : "46", "neto": "null"},{"produce": "Apples", "bruto" : "76", "neto": "null"}]} )
    # test__get_routes(url+"/session/35" ,'{"id": "35","truckID": "Truck1","items": [{"produce": "Oranges", "bruto" : "46", "neto": "null"},{"produce": "Apples", "bruto" : "76", "neto": "null"}]}')
    # test__get_routes(url+"/session/36" ,"""{"id": "36","truckID": "Truck1","items": [{"produce": "Tomato", "bruto" : "24", "neto": "null"},{"produce": "Test", "bruto" : "None", "neto": "null"}]}""")
    # test__get_routes(url+"/session/", "")

     # testing item route
    test_item_route('/item/truck1' ,{"id":"truck1","sessions":[35],"tara":92})
    

    # # testing get weight route
    # test__get_routes(url+"/weight?from=10000303000000&to=30000303000000&filter=in",'"35":{"bruto":"178","containers":"C1,C2","direction":"in","neto":"92","produces":"Apples,Oranges"},"36":{"bruto":"125","containers":"C1","direction":"In","neto":"12","produces":"Test,Tomato"}')
  

    #test_rout_weight(url+"/weight",{})
    #Testing Inserting Transaction with 3 containers using POST /weight
    timeIn=datetime.now().strftime("%Y%m%d%H%M%S")
    test_weightPost_route("/weight?direction=in&truck=DebugTruck&containers=C1%3APeaches%2BC1%3APeaches%2BC2%3ABananas&weight=390","<Response [200]>")
    test_weightPost_route("/weight?direction=none&truck=DebugTruck&containers=C1%3APeaches%2BC2%3ABananas&weight=308","<Response [200]>")
    test_weightPost_route("/weight?direction=none&truck=DebugTruck&containers=C2%3ABananas&weight=236","<Response [200]>")
    test_weightPost_route("/weight?direction=out&truck=DebugTruck&containers=&weight=150","<Response [200]>")
    timeOut=datetime.now().strftime("%Y%m%d%H%M%S")

    # # Testing if Transaction was entered successfully
    test_weightafterPost_route("/weight?from=%s&to=%s&filter=out"%(str(timeIn),str(timeOut)),'{"bruto":"390","containers":"C1,C2","direction":"Out","neto":"210","produces":"Bananas,Peaches"}')



    #testing batch-file route
    # test__post_routes(url+"/batch-weight?filename=containers3.json", "OK")
  

    # #testing /health route
    #test__get_routes(url+"/health", "OK")
    test_health()
    print(status)

    # #testing /unknown route
    #test__get_routes(url+"/unknown", "b'7  '")


main()
