from flask import Flask, Request, Response
from flask import request
import mysql.connector
from mysql.connector import Error
from insertions import read_json_file , read_csv_file
app = Flask(__name__)


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

@app.route('/weight' , methods=["GET"])
def get_weight():
    # Read the instructions
    return "OK"

@app.route('/item/<id>' , methods=["GET"])
def get_item(id):
    # Read the instructions
    return "OK"

if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0")
