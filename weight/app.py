from flask import Flask, Request, Response
import mysql.connector
from mysql.connector import Error


app = Flask(__name__)


def check_db_status(host='db',database='weightDB',user='user',password='alpine'):
    print("trying to connect...")
    #print("host:{}\n db:{}\n user:{}\n pass:{}".format(host,database,user,password))
    
    return mysql.connector.connect(password='alpine', user='root', host='db', port='3306', database='weightDB' ,  auth_plugin='mysql_native_password')


@app.route("/")
@app.route("/health")
def health():

    if check_db_status():
        return "Mysql connection"
    else:
        return "No Mysql connection"
    
    # Todo:
    # select 1 from db 
    '''
    print("enter to health\n")
    if (check_db_status()):
        return "OK" #response status = 200 'OK'
    
    else:
        return Response(status=400)

    '''
    print("Testing....")
    return "OK!!!"


if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0")
