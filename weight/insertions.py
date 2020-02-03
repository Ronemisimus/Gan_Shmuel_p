import csv
import json

def weight_to_kg(pounds):
    return int(pounds / 2.205)

# Read file in json format
#return list of tuples(id, weight, unit)
def read_json_file(filename):
    data = []
    weight_on_kg = 0
    with open(filename, 'r') as json_file:
        lines = json.load(json_file)
        for line in lines:
            if(line.get("unit") == "lbs"):
                weight_on_kg = weight_to_kg(int(line.get("weight")))
            else:
                weight_on_kg = line.get("weight")
            data.append( (line.get("id"), str(weight_on_kg)) )# tuple (container_id , container_weight_in_kg)
    return data

# Read file in csv format
#return list of tuples(id, weight)
def read_csv_file(filename):
    data = []
    weight_on_kg = 0
    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        title_line = next(csv_reader)
        unit = title_line[1]
        for line in csv_reader:
            if( unit == "lbs"):
                weight_on_kg = weight_to_kg(int(line[1]))
            else: 
                weight_on_kg = int(line[1])

            data.append((line[0], weight_on_kg))
    return data


tuples1 = read_csv_file('in/containers1.csv')
tuples2 = read_csv_file('in/containers2.csv')
tuples3 = read_json_file('in/containers3.json')

for line in tuples1:
    print (line)

for line in tuples2:
    print (line)

for line in tuples3:
    print (line)