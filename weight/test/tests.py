import requests
import os
from datetime import datetime


def validate(status, content, expected):
    code = 0
    log_info = ""
    if 500 <= status <= 599 :
        print("code is 500")
        log_info = "Status:  {}\n Content:\n{} \n Fail.\n".format(status, content)
        code = 1 
    else:
        if expected in content:
            log_info = "Status:  {}\n Content:\n{} \n \n".format(status, content)
        else:
            log_info = "Status:  {}\n Invalid Content:\n{}\n Expected: \n{} \n respone not as expected.\n".format(status, content, expected)
            code = 1
    return log_info , code







def test__get_routes(route, expected):
    res = requests.get(route)
    log , code  = validate(int(res.status_code), str(res.content), expected)
    with open("log.log", 'a+') as f:
        f.write("\n\n" + str(datetime.now()) + "\n\n")
        f.write("\nRoute:\t" + route + "\n\n" + log + "\n")
    if code == 1:
        print(1)
        exit()

def test__post_routes(route, expected):
    res = requests.post(route)
    log , code  = validate(int(res.status_code), str(res.content), expected)
    with open("log.log", 'a+') as f:
        f.write("\n\n" + str(datetime.now()) + "\n\n")
        f.write("\nRoute:\t" + route + "\n\n" + log + "\n")
    if code == 1:
        print(1)
        exit()



def main():
    # testing weight route
    test__get_routes(url+"/weight?from=10000303000000&to=30000303000000&filter=in",'"35":{"bruto":"178","containers":"C1,C2","direction":"in","neto":"92","produces":"Apples,Oranges"},"36":{"bruto":"125","containers":"C1","direction":"In","neto":"12","produces":"Test,Tomato"}')
    test__get_routes(url+"/weight?from=10000303000000&to=30000303000000",'"35":{"bruto":"178","containers":"C1,C2","direction":"in","neto":"92","produces":"Apples,Oranges"},"36":{"bruto":"125","containers":"C1","direction":"In","neto":"12","produces":"Test,Tomato"}')
    test__get_routes(url+"/weight?", "{")

    #testing /health route
    test__get_routes(url+"/health", "b'OK'")

    #testing /unknown route
    test__get_routes(url+"/unknown", "b'7  '")

    #testing session  route
    test__get_routes(url+"/session/35" ,'{"id": "35","truckID": "Truck1","items": [{"produce": "Oranges", "bruto" : "46", "neto": "null"},{"produce": "Apples", "bruto" : "76", "neto": "null"}]}')
    test__get_routes(url+"/session/36" ,"""{"id": "36","truckID": "Truck1","items": [{"produce": "Tomato", "bruto" : "24", "neto": "null"},{"produce": "Test", "bruto" : "None", "neto": "null"}]}""")
    test__get_routes(url+"/session/", "")

    # test_rout_weight(url+"/weight",{})

    # Testing Inserting Transaction with 3 containers using POST /weight
    timeIn=datetime.now().strftime("%Y%m%d%H%M%S")
    test__post_routes(url+"/weight?direction=in&truck=DebugTruck&containers=C1%3APeaches%2BC1%3APeaches%2BC2%3ABananas&weight=390","")
    test__post_routes(url+"/weight?direction=none&truck=DebugTruck&containers=C1%3APeaches%2BC2%3ABananas&weight=308","")
    test__post_routes(url+"/weight?direction=none&truck=DebugTruck&containers=C2%3ABananas&weight=236","")
    test__post_routes(url+"/weight?direction=out&truck=DebugTruck&containers=&weight=150","")
    timeOut=datetime.now().strftime("%Y%m%d%H%M%S")

     # testing item route
    test__get_routes(url+"/item/truck1", """id":"truck1","sessions":[35],"tara":92""")
    test__get_routes(url+"/item/c1","""{}""")
    test__get_routes(url+"/item/Truck1?from=20200202112732&to=20211231011500","""id":"Truck1","sessions":[35],"tara":92""")
   

    # Testing if Transaction was entered successfully
    test__get_routes(url+"/weight?from=%s&to=%s&filter=out"%(str(timeIn),str(timeOut)),'{"bruto":"390","containers":"C1,C2","direction":"Out","neto":"210","produces":"Bananas,Peaches"}')


    #testing batch-file route
    test__post_routes(url+"/batch-weight?filename=containers3.json", "b'OK inserted to db'")
    test__post_routes(url+"b'file not found or it already in database'", "b'OK inserted to db'")

    print(0)

url = "http://localhost:{}".format(os.environ['PORT'])
# url = "http://18.194.232.207:8089"


main()
