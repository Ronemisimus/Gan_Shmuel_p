from flask import Flask, request, Response
from datetime import datetime
from time import gmtime, strftime
import mysql.connector
from mysql.connector import Error
from insertions import read_json_file , read_csv_file
import json
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


#Convert yyyymmsddhhmmss to datetime object
def parse_time(t):
    # override t1 if argument was not supplided and equal None
    if not t:
        # Default t1 time is 1st of month at 000000
        year_format = datetime.date.today().replace(day=1)
        zero = datetime.time(0,00)
        t = datetime.combine(year_format ,zero)
    else:
        t = datetime.strptime(t , '%Y%m%d%H%M%S')
    
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
        t2 = datetime.strptime(t2 , '%Y%m%d%H%M%S')

    
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

	else:
		if request.args.get("from"):
			start = parse_time(request.args.get('from'))
		else:
			start = datetime.now().strftime("%Y-%m-%d 00:00:00")
		if request.args.get("to"):
			end = parse_time(request.args.get('to'))
		else:
			end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		# filt = request.args.get('filter').split(",") or "('in','out','none')"
		if request.args.get("f"):
			filt=("("+request.args.get("f")+")").replace("(","('").replace(",","','").replace(")","')")
		else:
			filt = "('in','out','none')"

		sql='''SELECT t2.TransactionID, t.Status, (SUM(t2.WeightProduce) + SUM(c.Weight)) AS bruto, SUM(t2.WeightProduce) AS neto, GROUP_CONCAT(DISTINCT t2.Produce) AS products, GROUP_CONCAT(DISTINCT t2.ContainerID) AS Containers
		FROM
			weightDB.Transactions t
		INNER JOIN weightDB.TruckContainers t2 ON
			t.ID = t2.TransactionID
		INNER JOIN weightDB.Containers c ON
			t2.ContainerID = c.ID
		WHERE
			t.TimeIn >= STR_TO_DATE('{}',
			'%Y-%m-%d %T')
			AND t.TimeOut <= STR_TO_DATE('{}',
			'%Y-%m-%d %T')
			AND t.Status IN {}
		GROUP BY
			t2.TransactionID'''.format(start, end, filt)
		TransactionsList = dbQuery(sql)
		rtn={}
		for tran in TransactionsList:
			rtn[str(tran[0])] = {'direction':str(tran[1]),'bruto':str(tran[2]),'neto': str(tran[3]),'produces':str(tran[4]),'containers':str(tran[5])}

		return rtn

if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0")
