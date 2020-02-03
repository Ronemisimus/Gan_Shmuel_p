from flask import Flask, request, Response
import mysql.connector
from mysql.connector import Error
from insertions import read_json_file , read_csv_file
import json
app = Flask(__name__)

def dbQuery(sql, isInsert):
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
    if ".csv" in filename:
        data = read_csv_file("in/" + filename)
    if ".json" in filename:
        data = read_json_file("in/" + filename)
    for tuple in data:
        dbQuery("INSERT INTO Containers (ID, Weight, Unit) VALUES ('"+ tuple[0] + "','" +  tuple[1] + "','" + tuple[2]+ "')", True)
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
    # Read the instructions
    return "OK"


@app.route("/weight", methods=['GET', 'POST'])
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

	transactionID="35"
	ContainersList=dbQuery('''SELECT t.id,t2.TruckID,t.Produce,(SUM(t.WeightProduce)+SUM(c.Weight)) AS Bruto,t.WeightProduce AS Neto
	FROM
		weightDB.TruckContainers t
	INNER JOIN weightDB.Transactions t2 ON
		t.TransactionID = t2.ID
	INNER JOIN weightDB.Containers c ON
		c.ID = t.ContainerID
	WHERE
		t.TransactionID = %s
	GROUP BY t.id'''%transactionID,False)
	# ContainersList=dbQuery("SELECT * FROM TruckContainers WHERE (TransactionID=%s)"%transactionID,False)

	rtn={}
	for con in ContainersList:
		rtn[str(con[0])] = {'truck':str(con[1]),'produce':str(con[2]),'bruto': str(con[3]),'neto':str(con[4])}

	return rtn

if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0")
