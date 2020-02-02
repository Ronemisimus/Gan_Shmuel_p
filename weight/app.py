from flask import Flask, Request, Response
import mysql.connector
from mysql.connector import Error
from datetime import datetime

app = Flask(__name__)

def dbQuery(sql):
    mydb = mysql.connector.connect(
    host='db',
    database='weightDB',
    user='root',
    password='alpine',
    port='3306'
    )
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    return mycursor.fetchall()

def dbInsert(sql):
    mydb = mysql.connector.connect(
    host='db',
    database='weightDB',
    user='root',
    password='alpine',
    port='3306'
    )
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    mydb.commit()
    return str(mycursor.lastrowid)

def check_db_status(host='db',database='weightDB',user='root',password='alpine'):
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

# @app.route("/weight", methods=['GET', 'POST'])
# def weight():
#     if Request.method == 'POST':
#         currtime = datetime.now()
#         direction = Request.values.get('direction')
#         truckID = Request.values.get('truckID')
#         containerIDs = Request.values.get('containers')
#         force = Request.values.get('username') or false
#         produce = Request.values.get('produce')

#     currtime = "1998-03-03 12:43:23"
#     direction = "in"
#     truckID = "T1ABD"
#     containerIDs = "C1,C2"
#     force = "false"
#     produce = "Oranges,Potatoes"
#     TransactionID = dbInsert("INSERT INTO Transactions (Status, TruckID, TimeIn) VALUES ('%s', '%s', '%s')"%(direction,truckID,currtime))
#     test2= dbQuery("SELECT * FROM Transactions")

#     return test

if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0")
