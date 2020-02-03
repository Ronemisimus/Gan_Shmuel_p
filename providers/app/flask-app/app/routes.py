import requests, json
from flask import request, jsonify, Response, json
from app import app, db
from app.models import Truck, Provider, Rate
from datetime import datetime, timezone

# comment init
def format_providers(providers):
  data = ''
  for provider in providers:
    data += 'ID: [{0}] - {1}: \n'.format(provider.id, provider.name)
  return data

def create_provider(provider_name):
  provider = Provider(name=provider_name)
  check_provider=provider.query.filter_by(name=provider_name).first()
  if check_provider is not None:
    return None
  else:
    db.session.add(provider)
    db.session.commit()
    return provider
  
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

# def test_truck():
#   res = requests.post('http://18.194.232.207:8087/truck', data={'truck': 'tester', 'provider_id': 10001})

@app.route('/health')
def health():
  try:
    db.session.execute('select 1')
    return 'db is alive'
  except:
    return Response(status=500)
@app.route('/')
def home():
    return 'Home page'

@app.route('/provider',methods =['POST'])
def provider():
  provider_name=request.form['provider']
  provider_res=create_provider(provider_name)
  if provider_res is None:
    return Response(json.dumps("Provider {} is already exists!".format(provider_name)),mimetype='application/json')
  
  res={'ID':provider_res.id}
  return Response(json.dumps(res),mimetype='application/json')

@app.route('/provider/<provider_id>' , methods=['PUT'])
def updateProvider(provider_id):
  provider_new_name=request.args.get('provider_name')
  if Provider.query.filter_by(name=provider_new_name).first() is None: 
    search_provider_id=Provider.query.filter_by(id=provider_id).first()
    if search_provider_id is None:
      return Response(json.dumps("Provider {} is not exist! ".format(provider_id)),mimetype='application/json')
    search_provider_id.name=provider_new_name
    db.session.commit()
    return Response(json.dumps("Provider {} new name is {}".format(search_provider_id.id,search_provider_id.name)),mimetype='application/json')
  else:
    return Response(json.dumps("Provider name {} already exist ,cant accpet new name!".format(provider_new_name)),mimetype='application/json')
  
    
@app.route('/truck', methods=['POST'])
def truck():
    test_truck()
    provider_id = request.args.get('provider_id')
    truck_id = request.args.get('truck')
    res_provider = Provider.query.filter_by(id=provider_id).first()
    if res_provider is None:
      return Response(json.dumps('Provider ({}) Not Found'.format(provider_id)),mimetype='application/json')
    try:
      new_truck = Truck(id=truck_id, truck_provider=res_provider)
    except:
      return Response(status=500)
    db.session.add(new_truck)
    db.session.commit()
    res_truck = {
      'id': new_truck.id,
      'provider_id': new_truck.provider_id
    }
    return Response(json.dumps(res_truck), mimetype="application/json")

@app.route('/truck/<truck_id>', methods=['GET', 'PUT'])
def update_truck(truck_id):
    if request.method == 'PUT':
      provider_id = request.args.get('provider_id')
      res_provider = Provider.query.filter_by(id=provider_id).first()
      if res_provider is None:
        return Response(json.dumps('Provider ({}) Not Found'.format(provider_id)),mimetype='application/json')
      
      truck = Truck.query.filter_by(id=truck_id).first()
      if truck is None:
        return Response(json.dumps('Truck ({}) Not Found'.format(truck_id)),mimetype='application/json')
        
      truck.provider_id = provider_id
      db.session.commit()
      res_truck = {
        'id': truck.id,
        'provider_id': truck.provider_id
      }
      return Response(json.dumps(res_truck), mimetype="application/json")
    elif request.method == 'GET':
      truck = Truck.query.filter_by(id=truck_id).first()
      if truck is None
        return Response(status=404)

      from_date = parse_time(request.args.get('from'))

      to_param = request.args.get('to') 
      to_date = datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S') if to_param is None else to_param
      base_url = 'http://18.194.232.207:8089/'
      item_url = '{0}item/{1}'.format(base_url, truck.id)
      res = requests.post(item_url, data={'form': from_date, 'to': to_date})

      return Response(res)