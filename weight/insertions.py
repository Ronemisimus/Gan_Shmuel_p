import csv
import sys
import json

# Read file in json format
def read_json_file(filename):
    return True
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
        for line in data:
            # print (line.get("id") + " weight " + str(line.get("weight")) + " units " + line.get("unit"))
            insertVariblesIntoTable(line.get("id"), line.get("weight"), line.get("unit"))

# Read file in csv format
def read_csv_file(filename):
    with open(filepath, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        title_line = next(csv_reader)
        unit = title_line[1]
        for line in csv_reader:
            insertVariblesIntoTable(line[0], int(line[1]), unit)

