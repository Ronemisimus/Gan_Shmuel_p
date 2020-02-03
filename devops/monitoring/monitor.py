import requests
from flask import Flask
import time

#some comment :)

app = Flask(__name__)

@app.route('/monitor')
def monitor():
    services = {
        'prd-weight':'8089',
        'stg-weight':'8088',
        'prd-provider':'8087',
        'stg-provider':'8086',
        'ci-server':'8085'
    }
    paths = ['/','/health']

    #the beginning of the messgae to print is html script that refreshes the page every 30 second
    printM = '<meta http-equiv="refresh" content="30">'  

    while True:
        for service in services:
            for path in paths:
                try:
                    response = requests.get('http://18.194.232.207:'+services[service]+path) #make sure the request is not made localy
                    if response.status_code == 200:
                        printM += (service+path+' is up!<br>')
                    else:
                        printM += (service+path+' returned:'+response.status_code+'<br>')
                except:
                    printM += (service+path+' is unreachable<br>')
            
        printM += time.ctime()
        return printM
        

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=8083, threaded=True, debug=True)