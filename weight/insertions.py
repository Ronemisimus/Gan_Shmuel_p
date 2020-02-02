import mysql.connector
import csv
import sys
import json
from mysql.connector import Error

def usage():
    print("""\
        Runing app:
        insertions.py <path to file>
        Please ensure that file path correct and file exist   
    """)
    exit()

def read_json_file(filename):
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
        for line in data:
            # print (line.get("id") + " weight " + str(line.get("weight")) + " units " + line.get("unit"))
            insertVariblesIntoTable(line.get("id"), line.get("weight"), line.get("unit"))


def read_csv_file(filename):
    with open(filepath, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        title_line = next(csv_reader)
        unit = title_line[1]
        for line in csv_reader:
            insertVariblesIntoTable(line[0], int(line[1]), unit)


def insertVariblesIntoTable(cont_id, weight, unit):
    try:
        print("insert to table values: c_id " + cont_id + "  weight   " + str(weight) + "  unit " + unit)
    #     connection = mysql.connector.connect(host='localhost:8081',
    #                                          database='weightDB',
    #                                          user='user',
    #                                          password='alpine')
    #     cursor = connection.cursor()
    #     mySql_insert_query = """INSERT INTO containers (cont_id, weight, unit) 
    #                             VALUES (%s, %s, %s) """

    #     recordTuple = (cont_id, weight, unit)
    #     cursor.execute(mySql_insert_query, recordTuple)
    #     connection.commit()
    #     print("Record inserted successfully into containers table")

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    # finally:
    #     if (connection.is_connected()):
    #         cursor.close()
    #         connection.close()
    #         print("MySQL connection is closed")


# main 
if(len(sys.argv) !=  2):
    usage()
else:
    filepath = sys.argv[1]
    try:
        if ".csv" in filepath:
            read_csv_file(filepath)
        if ".json" in filepath:
            read_json_file(filepath)
    except:
        usage()

print("Insertion is done")