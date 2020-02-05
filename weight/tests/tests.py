import requests
import os
from datetime import datetime


def validate(status, content, expected):
    code = 0
    log_info = ""
    if status >= 500 or status <= 599 :
        log_info = "Status:  {}\n Content:\n{} \n Fail.\n".format(status, content)
        code = 1 
    else:
        if expected in content:
            log_info = "Status:  {}\n Content:\n{} \n \n".format(status, content)
        else:
            log_info = "Status:  {}\n Invalid Content:\n{}\n Expected: \n{} \n respone not as expected.\n".format(status, content, expected)
            code = 1
    return log_info , code







def test__get_routes(route, expected ):
    res = requests.get(route)
    log , code  = validate(res.status_code, res.content, expected)
    with open("log.log", 'a+') as f:
        f.write("\n\n" + str(datetime.now()) + "\n\n")
        f.write("\nRoute:\t" + route + "\n\n" + log + "\n")
    if code == 1:
        print(1)
        exit()

def test__post_routes():
    # 
    pass



def main():
    test__get_routes(url+"/weight?from=10000303000000&to=30000303000000&f=in",'{"35":{"bruto":"178","containers":"C1,C2","direction":"in","neto":"92","produces":"Apples,Oranges"},"36":{"bruto":"125","containers":"C1","direction":"In","neto":"12","produces":"Test,Tomato"}}')
    test__get_routes(url+"/weight?from=10000303000000&to=30000303000000",'{"35":{"bruto":"178","containers":"C1,C2","direction":"in","neto":"92","produces":"Apples,Oranges"},"36":{"bruto":"125","containers":"C1","direction":"In","neto":"12","produces":"Test,Tomato"}}')


    # test_rout_weight(url+"/weight",{})

    print(0)

url = "http://localhost:{}".format(os.environ['PORT'])
# url = "http://18.194.232.207:8089"


main()