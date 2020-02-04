import requests, json
from flask import request, jsonify, Response, json, redirect, url_for
from app import app, db
from app.models import Truck, Provider, Rate
from datetime import datetime, timezone


def create_provider(provider_name):
  provider = Provider(name=provider_name)
  check_provider=provider.query.filter_by(name=provider_name).first()
  if check_provider is not None:
    return None
  else:
    db.session.add(provider)
    db.session.commit()
    return provider

def test_health():
  try:
    res = db.session.execute('show tables')
    res_str = res.fetchall()
    res_str = str(res_str)
    return Response(res_str, status=200)
  except:
    return Response(status=500)

@app.route('/health')
def health():
  return test_health()
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
      return Response("Provider {} is not exist! ".format(provider_id),mimetype='text/plain', status=404)
    search_provider_id.name=provider_new_name
    db.session.commit()
    return Response(json.dumps("Provider {} new name is {}".format(search_provider_id.id,search_provider_id.name)),mimetype='application/json')
  else:
    return Response(json.dumps("Provider name {} already exist ,cant accpet new name!".format(provider_new_name)),mimetype='application/json')
  
    
@app.route('/truck', methods=['POST'])
def truck():
  provider_id = request.form['provider_id']
  truck_id = request.form['truck']
  res_provider = Provider.query.filter_by(id=provider_id).first()
  if res_provider is None:
    return Response(json.dumps('Provider ({}) Not Found'.format(provider_id)),mimetype='application/json', status=404)
  try:
    new_truck = Truck(id=truck_id, truck_provider=res_provider)
  except Exception as e:
    return Response(str(e), status=500)
  try:
    db.session.add(new_truck)
    db.session.commit()
  except Exception as e:
    return Response(str(e), status=500)
  res_truck = {
    'id': new_truck.id,
    'provider_id': new_truck.provider_id
    }
  return Response(json.dumps(res_truck), mimetype="application/json")

@app.route('/truck/<truck_id>', methods=['GET', 'PUT'])
def update_truck(truck_id):
    if request.method == 'PUT':
      provider_id = request.form['provider_id']
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
      if truck is None:
        return Response('Truck ({}) Not Found'.format(truck_id), status=404)

      to_param = request.args.get('to')
      if to_param is None or to_param == '':
        to_param = datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')

      try:
        from_date = str(datetime.strptime(str(request.args.get('from')), '%Y%m%d%H%M%S'))
        to_date = str(datetime.strptime(str(to_param), '%Y%m%d%H%M%S'))
      except Exception as e:
        return Response(str(e), status=400)
      base_url = 'http://18.194.232.207:8088/'
      item_url = '{0}item/{1}'.format(base_url, truck.id)
      # try:
      #   res = requests.get(item_url, data={'from': from_date, 'to': to_date})
      # except Exception as e:
      #   return Response(str(e))

      data = {
        "id": "test_id",
        "tara": 50,
        "sessions": [14, 54, 60]
      }
      temp_json = json.dumps(data);
      return Response(temp_json, mimetype="application/json")
      # return Response(res, mimetype='application/json')