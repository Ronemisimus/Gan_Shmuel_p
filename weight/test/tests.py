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

def main():
    test_health()
    test_unknown('/unknown' ,{"7":{"ContainerID":"C1","Produce":"Test","TransactionID":"36"}} )

    print(status)

main()
