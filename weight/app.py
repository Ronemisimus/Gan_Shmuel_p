from flask import Flask, request, Response
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


#Convert yyyymmsddhhmmss to datetime object
def parse_time(t):
    # override t1 if argument was not supplided and equal None
    if not t:
        # Default t1 time is 1st of month at 000000
        year_format = datetime.date.today().replace(day=1)
        zero = datetime.time(0,00)
        t = datetime.datetime.combine(year_format ,zero)
    else:
        t = datetime.datetime.strptime(t , '%Y%m%d%H%M%S')
    
    return t



@app.route('/item/<id>' , methods=["GET"])
def get_item(id):

    # Get the id for an item(truck or container)   
    trackId = dbQuery('select * from Transactions where TruckID="{}"'.format(id))

    # if truck or container does not exists
    if not (trackId):
        return Response(status="404")


    t1 = request.args.get('from')
    t1 = parse_time(t1)

    # Default t2 time- now
    t2 = request.args.get('to')
    
    # override the t2 time
    if not t2:
        t2 = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    else:
        t2 = datetime.datetime.strptime(t2 , '%Y%m%d%H%M%S')

    
    sessions_result_list = dbQuery('''SELECT t.TruckID, SUM(t2.WeightProduce), t.ID
    FROM
        weightDB.Transactions t
    INNER JOIN weightDB.TruckContainers t2 ON
        t2.TransactionID = t.ID
    WHERE
        t.TruckID = "{}"
        AND t.TimeIn >= STR_TO_DATE('{}','%Y-%m-%d %T')
        AND t.TimeOut <= STR_TO_DATE('{}','%Y-%m-%d %T')
    GROUP BY
        t.ID'''.format(trackId,str(t1),str(t2)),False)
    
    return str(len(sessions_result_list))
    


app.route("/weight", methods=['GET', 'POST'])
def weight():
	if request.method == 'POST':
		return "post"
    #     currtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #     direction = Request.values.get('direction')
    #     truckID = Request.values.get('truckID')
    #     containerIDs = Request.values.get('containers')
    #     force = Request.values.get('username') or false
    #     produce = Request.values.get('produce')
    #     if(direction == "in"):
    #     	TransactionID = dbQuery("INSERT INTO Transactions (Status, TruckID, TimeIn) VALUES ('%s', '%s', '%s')"%(direction,truckID,currtime), True)
    #     else:
    #     	dbQuery("UPDATE Transactions SET TimeOut = %s WHERE TruckID = %s AND Status = 'in'"%(currtime,truckID),True)

	test2= dbQuery("SELECT * FROM Transactions", False)

	return str(test2[0][2])

if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0")
