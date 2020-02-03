from flask import Flask, Request, Response
from flask import request
import datetime
from time import gmtime, strftime
import mysql.connector
from mysql.connector import Error
from insertions import read_json_file , read_csv_file
app = Flask(__name__)

def dbQuery(sql, isInsert=None):
    mydb = mysql.connector.connect(
    host='db',
    database='weightDB',
    user='root',
    password='alpine',
    port='3306'
    )
    mycursor = mydb.cursor()
    mycursor.execute(sql)

    if isInsert:
    	mydb.commit()
    	return str(mycursor.lastrowid)
    else:
    	return mycursor.fetchall()

# Todo: See how we can instantiate the DB only once , and pass it to app.py
def check_db_status(host='db',database='weightDB',user='user',password='alpine'):
    return mysql.connector.connect(password='alpine', user='root', host='db', port='3306', database='weightDB' ,  auth_plugin='mysql_native_password')


# Entery points
@app.route("/")
@app.route("/health")
def health():
    if check_db_status():
        return Response(status=200)
    else:
        return Response(status=500)

@app.route('/batch-weight-file<string:filename>' , methods=["POST"])
def batch_weight(filename):
    # Will upload list of tara weights from a file in "/in" folder. Usually used to accept a batch of new containers. 
    # File formats accepted: csv (id,kg), csv (id,lbs), json ([{"id":..,"weight":..,"unit":..},...])
    return "OK"

@app.route('/unknown' , methods=["GET"])
def unknown():
    # Returns a list of all recorded containers that have unknown weight:
    # ["id1","id2",...]
    return "OK"

@app.route('/session/<id>' , methods=["GET"])
def session(id):
    # Read the instructions
    return "OK"

@app.route('/item/<id>' , methods=["GET"])
def get_item(id):

    # Get the id for an item(truck or container)   
    transactionId = dbQuery('select * from TruckContainers where id={}'.format(id))
    trackId = dbQuery('select * from Transactions where TruckID={}'.format(id))

    # if truck or container does not exists
    if not (transactionId or trackId):
        return Response(status="404")
    
    # from time
    t1 = request.args.get('from') if request.args.get('from') else  datetime.date.today().replace(day=1)
    zero = datetime.time(0,00)
    t1 = datetime.datetime.combine(t1 ,zero)

    # to time
    t2 = request.args.get('to') if request.args.get('to') else strftime("%Y-%m-%d %H:%M:%S", gmtime()) 


    return "from - {} to - {} ".format(t1 , t2)
    
    
    #return "OK"


# @app.route("/weight", methods=['GET', 'POST'])
# def weight():
#     if Request.method == 'POST':
#         currtime = datetime.now()
#         direction = Request.values.get('direction')
#         truckID = Request.values.get('truckID')
#         containerIDs = Request.values.get('containers')
#         force = Request.values.get('username') or false
#         produce = Request.values.get('produce')

    # currtime = "1998-03-03 12:43:23"
    # direction = "in"
    # truckID = "T1ABD"
    # containerIDs = "C1,C2"
    # force = "false"
    # produce = "Oranges,Potatoes"
    # TransactionID = dbQuery("INSERT INTO Transactions (Status, TruckID, TimeIn) VALUES ('%s', '%s', '%s')"%(direction,truckID,currtime), True)
    # test2= dbQuery("SELECT * FROM Transactions", False)

    # return str(test2[0][2])

if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0")
