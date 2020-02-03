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
    

# @app.route('/providers', methods=['GET', 'POST'])
# def chat(provider=None):
#   return render_template("index.html", provider=provider)

# @app.route('/api/<provider>', methods=['GET', 'POST'])
# def get_providers(provider=None):
#   res_provider = Provider.query.filter_by(name=provider).first()
#   if res_provider is None:
#     new_provider = create_provider(provider)
#     res_provider = Provider.query.filter_by(name=provider).first()

#   # if request.method == 'POST':
#   #   username = request.form.get('username')
#   #   msg = request.form.get('msg')
#   #   new_post = Post(msg=msg, room_id=res_room.room_id, username=username)
#   #   db.session.add(new_post)
#   #   db.session.commit()

#   # posts = Post.query.filter_by(room_id=res_room.room_id).all()
#   providers = Provider.query.all()
#   res_prov = format_providers(providers);
  
#   try:
#     return res_prov
#   except:
#     return Response(status=500)