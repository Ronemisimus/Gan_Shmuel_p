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
        if content in expected:
            log_info = "Status:  {}\n Content:\n{} \n \n".format(status, content)
        else:
            log_info = "Status:  {}\n Content:\n{} \n respone not as expected.\n".format(status, content)
            code = 1
    return log_info , code







def test__get_routes(route, expected ):
    res = requests.get(route)
    log , code  = validate(res.status_code, res.content, expected)
    with open("log.log", 'a+') as f:
        f.write("\n\n" + str(datetime.now()) + "\n\n")
        f.write("\nRoute:\t" + route + "\nValidation Data: \t" + item + "\n" + log + "\n")
    if code == 1:
        print(1)
        exit()

def test__post_routes():
    # 
    pass



def main():
    test__get_routes(url+"/weight",{})
    test_rout_weight(url+"/weight")

    print(0)

url = "http://localhost:{}".format(os.environ['PORT'])

main()