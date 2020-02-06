import requests
from flask import Flask
from datetime import datetime, timezone
import pytz

app = Flask(__name__)

printM = '' 

@app.route('/monitor')
def monitor():
    global printM
    #the beginning of the messgae to print is html script that refreshes the page every 30 second
    printM = '<meta http-equiv="refresh" content="30">'

    services = {
        'prd-weight':'8089',
        'stg-weight':'8088',
        'prd-provider':'8087',
        'stg-provider':'8086'
    }
    paths = ['/','/health']

    dev_services = {
        'ci-server':'8085',
        'reports-server':'8084'
    }

    dev_paths = ['/health'] 

    def check(services, service, path):
        global printM
        url = 'http://18.194.232.207:'+services[service]+path
        htmlS = '<a href='+url+' style="color:#4682B4">'+service+path+'</a>'
        try:   
            response = requests.get(url) #make sure the request is not made localy
            if response.status_code == 200:
                printM += ('<span style="color:#006400">'+htmlS+' is up!</span><br>')
            else:
                printM += (htmlS+' returned:'+response.status_code+'<br>')
        except:
            printM += ('<span style="color:#8B0000"><b>'+htmlS+' is unreachable</b></span><br>')

    while True:
        for service in services:
            for path in paths:
                check(services, service, path)

        for dev_service in dev_services:
            for dev_path in dev_paths:
                check(dev_services, dev_service, dev_path)

        tz = pytz.timezone('Asia/Jerusalem')
        isr_now = datetime.now(tz)
        printM += ('<p style="color:#191970"> Last updated: {}</p>'.format(isr_now))
        return printM
        

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=8083, threaded=True, debug=True)