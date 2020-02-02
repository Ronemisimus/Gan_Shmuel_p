from flask import Flask, Request, Response
import mysql.connector
from mysql.connector import Error


app = Flask(__name__)


def check_db_status(host='localhost',database='Electronics',user='root',password='123'):

    #print("host:{}\n db:{}\n user:{}\n pass:{}".format(host,database,user,password))
    '''
    try:
        connection = mysql.connector.connect(host=host,
                                         database=database, #Example DB = 'Electronics'
                                         user=user,
                                         password=password)

        if connection.is_connected():
            connection.close()
            return True
    except:
        return False
    '''
    return True

@app.route("/")
@app.route("/health")
def health():
    if (check_db_status()):
        return "OK" #response status = 200 'OK'
    
    else:
        return Response(status=400)


if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0")
