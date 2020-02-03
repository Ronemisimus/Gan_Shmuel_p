import csv
import json

# Read file in json format
#return list of tuples(id, weight, unit)
def read_json_file(filename):
    data = []
    with open(filename, 'r') as json_file:
        lines = json.load(json_file)
        for line in lines:
            data.append((line.get("id"), str(line.get("weight")), line.get("unit")))
    return data

# Read file in csv format
#return list of tuples(id, weight, unit)
def read_csv_file(filename):
    data = []
    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        title_line = next(csv_reader)
        unit = title_line[1]
        for line in csv_reader:
            data.append((line[0], line[1], unit))
    return data
