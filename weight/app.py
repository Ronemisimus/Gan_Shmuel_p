from flask import Flask, request, Response, render_template, send_from_directory
from datetime import datetime , time 
from time import gmtime, strftime
import mysql.connector
from mysql.connector import Error
from insertions import read_json_file , read_csv_file
import json
import os
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

@app.route("/favicon.ico", methods=["GET"])
def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Entery points
@app.route("/")
@app.route("/health")
def health():
    if check_db_status():
        return "OK"
    else:
        return Response(status=500)

@app.route('/batch-weight' , methods=["POST"])
def batch_weight():
    filename = request.form.get('filename')
    try:
        # Will upload list of tara weights from a file in "/in" folder. Usually used to accept a batch of new containers. 
        # File formats accepted: csv (id,kg), csv (id,lbs), json ([{"id":..,"weight":..,"unit":..},...])
        if ".csv" in filename:
            data = read_csv_file("in/" + filename)
        if ".json" in filename:
            data = read_json_file("in/" + filename)
        for tuple in data:
            dbQuery("INSERT INTO Containers (ID, Weight) VALUES ('"+ tuple[0] + "','" +  str(tuple[1]) +"')", True)
        return "OK inserted to db"
    except:
        return "file not found or it already in database", 404

   

@app.route('/unknown' , methods=["GET"])
def unknown():
    # Returns a list of all recorded containers that have unknown weight:
    # "id1" "id2"
    unknown_containers = ""
    data = dbQuery("SELECT * FROM Containers WHERE Weight is NULL", isInsert=False)
    for tuple in data:
        unknown_containers = unknown_containers + tuple[0] + '  '
    return unknown_containers

@app.route('/session/<id>' , methods=["GET"])
def session(id):
    # method get session id and return json in format:
    # [{
    # 	"id": "<id>",
    # 	"truckID": "<truck id>",
    # 	"items":
    #  [{
    # 		"produce": "<type of produce>",
    # 		"bruto": "<weight bruto>",
    # 		"neto": "<weight_neto| null>"
    # 	}]
    # }]
    # get table [ Produse | Bruto | Neto | Status | Truck ]
    query = """ SELECT
            t.Produce,
            (SUM(t.WeightProduce) + SUM(c.Weight)) AS bruto,
            SUM(t.WeightProduce) AS neto,
            t2.Status,
            t2.TruckID
        FROM
            weightDB.TruckContainers t
        INNER JOIN weightDB.Containers c ON
            c.ID = t.ContainerID
        INNER JOIN weightDB.Transactions t2 ON
            t.TransactionID = t2.ID
        WHERE
            t2.ID ={}
        GROUP BY
            t.Produce""".format(str(id))
    data = dbQuery(query,False)
    if len(data) == 0 :
        return Response(status = "404")
    else :
        json = '[{"id": "' + str(id) + '","truckID": "' + str(data[0][4]) + '","items": ['
        for tuple in data:
            if tuple[3] != "out":
                json += '{' +'"produce": "{}", "bruto" : "{}", "neto": "{}"'.format(tuple[0],tuple[1], "null")+ '},'
            else:
                json += '{' +'"produce": "{}", "bruto" : "{}", "neto": "{}"'.format(tuple[0],tuple[1], tuple[2])+ '},'
        json  = json[:-1] +  ']}]' 
    return json


#Convert yyyymmsddhhmmss to datetime object
def parse_time(t):
    # override t1 if argument was not supplided and equal None
    if not t:
        # Default t1 time is 1st of month at 000000
        year_format = datetime.today().replace(day=1)
        zero = time(00,00,00)
        t = datetime.combine(year_format ,zero)
    else:
        t = datetime.strptime(t , '%Y%m%d%H%M%S')
    
    return t




@app.route('/item/<id>' , methods=["GET"])
def get_item(id):

    # if id was not provided
    if not id:
        return Response(status=404) 


    try:
        #if id is int dealing with containers
        id = int(id)
        ans = dbQuery("SELECT * FROM TruckContainers where id = {} ".format(id), isInsert=False)
       
        #if id is not exist
        if not len(ans):
            return Response(status = 404)  
        

        data =dbQuery('''SELECT
                        t2.id,
                        t2.WeightProduce,
                        t2.TransactionID
                    FROM
                        weightDB.TruckContainers t2
                    INNER JOIN weightDB.Transactions t ON
                    t2.TransactionID = t.ID
                    WHERE
                    t.TimeIn >= STR_TO_DATE('1997-12-01 12:00:00',
                    '%Y-%m-%d %T')
                    AND t.TimeOut <= STR_TO_DATE('2021-12-01 12:00:00',
                    '%Y-%m-%d %T')
                    AND t2.id = {};'''.format(id), isInsert=False)
        
        return {"id":str(id) , "tara":data[0][1] , "sessions":data[0][2]}
        



        
    except:
        #id is a string, dealing with trucks
        t1 = request.args.get('from')
        t1 = parse_time(t1)

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
            t.ID'''.format(str(id),str(t1),str(t2)))

        if not len(sessions_result_list):
            return {}

        sesseions_array = []
        tara = int(sessions_result_list[0][1])

    
        for result in sessions_result_list:
            sesseions_array.append(result[2])
        
        return {"id":str(id) , "tara":tara , "sessions":sesseions_array}
        

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

@app.route("/input", methods=['GET'])
def input():
	return render_template('weight_form.html')

if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0")
