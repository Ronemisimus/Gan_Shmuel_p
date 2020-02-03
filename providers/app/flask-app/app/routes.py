import requests
import json
from flask import render_template, request, jsonify, Response, json ,redirect ,Request
from app import app
from app import db
from app.models import Truck, Provider, Rate

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
  else:
    res={'ID':provider_res.id}
    return Response(json.dumps(res),mimetype='application/json')
    
@app.route('/truck', methods=['POST'])
def truck():
    provider_id = request.args.get('provider_id')
    truck_id = request.args.get('truck')
    res_provider = Provider.query.filter_by(id=provider_id).first()
    if res_provider is None:
      return 'Provider ({}) Not Found'.format(provider_id)
    try:
      new_truck = Truck(id=truck_id, provider_id=provider_id)
    except:
      return Response(status=500)
    db.session.add(new_truck)
    db.session.commit()
    res_truck = {
      'id': new_truck.id,
      'provider_id': new_truck.provider_id
    }
    return Response(json.dumps(res_truck), mimetype="application/json")

@app.route('/truck/<truck_id>', methods=['PUT'])
def update_truck(truck_id):
    print(truck_id)
    provider_id = request.args.get('provider_id')
    res_provider = Provider.query.filter_by(id=provider_id).first()
    if res_provider is None:
      return 'Provider ({}) Not Found'.format(provider_id)
    
    truck = Truck.query.filter_by(id=truck_id).first()
    if truck is None:
      return 'Truck ({}) Not Found'.format(truck_id)
      
    truck.provider_id = provider_id
    db.session.commit()
    res_truck = {
      'id': truck.id,
      'provider_id': truck.provider_id
    }
    return Response(json.dumps(res_truck), mimetype="application/json")