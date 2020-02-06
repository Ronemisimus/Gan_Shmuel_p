import requests, json
from flask import request, jsonify, Response, json, redirect, url_for, send_file, render_template
from app import app, db
from app.models import Truck, Provider, Rate
from datetime import datetime, timezone
import xlrd, os, sys

allowed_ext = ['csv', 'xls', 'xlsx']
base_url = 'http://18.194.232.207:8088/'
volume_path=os.getcwd()+'/in/'
full_path=''

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
    return render_template('index.html')

@app.route('/provider',methods =['POST'])
def provider():
  provider_name=request.form['provider']
  provider_res=create_provider(provider_name)
  if provider_res is None:
    return Response(json.dumps("Provider {} is already exists!".format(provider_name)),mimetype='application/json',status=400)
  
  res={'id':provider_res.id, 'name':provider_res.name}
  return Response(json.dumps(res),mimetype='application/json')

@app.route('/provider/<provider_id>' , methods=['PUT'])
def updateProvider(provider_id):
  provider_new_name=request.form['provider_name']
  if Provider.query.filter_by(name=provider_new_name).first() is None: 
    search_provider_id=Provider.query.filter_by(id=provider_id).first()
    if search_provider_id is None:
      return Response("Provider {} is not exist! ".format(provider_id),mimetype='text/plain', status=400)
    search_provider_id.name=provider_new_name
    db.session.commit()
    res = {'id': search_provider_id.id, 'name': provider_new_name}
    return Response(json.dumps(res),mimetype='application/json')
  else:
    return Response(json.dumps("Provider name {} already exist ,cant accpet new name!".format(provider_new_name)),mimetype='application/json',status=400)
  
    
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
      global base_url
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
      item_url = '{0}item/{1}'.format(base_url, truck.id)
      try:
        res = requests.get(item_url, data={'from': from_date, 'to': to_date})
        res = json.dumps(res.json())
      except Exception as e:
        return Response(str(e))

      return Response(res, mimetype='application/json')

@app.route('/bill/<id>')
def getBill(id):
  global base_url
  provider_id=Provider.query.filter_by(id=id).first()
  if provider_id is None:
    return Response(json.dumps('Provider ({}) Not Found'.format(id)),mimetype='application/json')
  provider_name=Provider.query.filter_by(id=id).first()
  product_amount = {}
  product_session_count = {}
  products_list=[]
  truck_count=0
  session_count=0
  from_date=request.args.get('from')
  try:
    from_date = str(datetime.strptime(str(request.args.get('from')), '%Y%m%d%H%M%S'))
  except Exception as e:
    return Response(str(e), status=400)
  to_param=request.args.get('to')
  to_date = datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S') if to_param is None else to_param
  trucks_of_provider=Truck.query.filter_by(provider_id=id).all()
  if not trucks_of_provider:
    return Response(json.dumps("Provider {} has no truck regiseted".format(provider_id)),mimetype='application/json')
  else:
    provider_name=Provider.query.filter_by(id=id).first()
    product_amount = {}
    product_session_count = {}
    products_list=[]
    truck_count=0
    session_count=0
    from_date=request.args.get('from')
    to_param=request.args.get('to')
    to_date = datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S') if to_param is None else to_param
    trucks_of_provider=Truck.query.filter_by(provider_id=id).all()
    for truck in trucks_of_provider:
      truck_count+=1
      item_url = '{0}item/{1}'.format(base_url, truck.id)
      try:
        res = requests.get(item_url, data={'from': from_date, 'to': to_date})
        res = res.json()
      except Exception as e:
        return Response(str(e))
      else:
        for session in res['sessions']:
          session_count+=1
          try:
            res_session=requests.get('{}session/{}'.format(base_url,session))
          except Exception as e:
            return Response(str(e))
          res_session=res_session.json()
          for product in res_session['items']:
            if product['produce'] in product_session_count:
              product_session_count[product['produce']]+=1
            else:
              product_session_count[product['produce']]=1
            if product['produce'] in product_amount:
              product_amount[product['produce']]+=product['bruto']
            else:
              product_amount[product['produce']]=product['bruto']
    total_pay=0
    generic_scope='ALL'
    for key in product_session_count:
      if Rate.query.filter_by(product_id=key , scope=id) is None:
        if Rate.query.filter_by(product_id=key , scope=provider_name.name) is None:
          rate=Rate.query.filter_by(product_id=key , scope=generic_scope).first()
      else:
        rate=Rate.query.filter_by(product_id=key , scope=id).first()
      print(type(rate), file=sys.stderr)
      print(rate.rate)
      print(type(product_amount[key]))
      product_details={'product':key ,'count':product_session_count[key],'amount':product_amount[key],'rate':rate.rate,'pay':(rate.rate*int(product_amount[key]))}
      total_pay+=product_details['pay']
      products_list.append(product_details)
  res_data = {
    'ID':id ,
    'Name':provider_name.name,
    'From':from_date,
    'To':to_date,
    'Truck_count':truck_count,
    'Session_Count':session_count,
    'Products':products_list ,
    'Total':total_pay}
  print(res_data)
  return Response(json.dumps(res_data),mimetype='application/json')



@app.route('/rates', methods=['GET' , 'POST'])
def rates():
  global filename, volume_path, allowed_ext, full_path
  if request.method=='POST':
    rate_list = []
    try:
      filename=request.form['file']
      file_ext = filename.split('.')[-1]
      if file_ext not in allowed_ext:
        return Response('File type is not allowed ({})'.format(file_ext), status=400)
    except:
      return "No file name was given. Please mention wanted file's name inside the form."
    finally:
      full_path=volume_path+filename
    try:
      book = xlrd.open_workbook(full_path, on_demand=True)
    except:
      return Response("File ({}) not found in folder".format(filename), status=404)
    else: ## Case file was opend successfuly
      sheet = book.sheet_by_index(0) ## ToDo: change to find sheet by name
      for rownum in range(1,sheet.nrows):
        temp_obj={}
        temp_rate={}
        for col in range(0, sheet.ncols):
          col_name = sheet.col_values(col)[0].lower()
          value = sheet.row_values(rownum)[col]  if col_name != 'product' else str(sheet.row_values(rownum)[col]).split('.')[0]
          temp_obj[col_name] = value
        new_rate = Rate(product_id=temp_obj['product'], scope=temp_obj['scope'], rate=temp_obj['rate'])
        exist_rate = Rate.query.filter_by(product_id=new_rate.product_id, scope=new_rate.scope).first()
        if exist_rate is None:
          db.session.add(new_rate)
          temp_rate=new_rate.serialize
        else:
          exist_rate.rate = new_rate.rate
          temp_rate=exist_rate.serialize
        try:
          db.session.commit()
        except Exception as e:
          msg = 'Could not insert new rate({})\n{}\n'.format(temp_obj, e)
          return Response(msg, status=400)
        else:
          rate_list.append(temp_rate)
    book.release_resources()
    del book
    return Response(json.dumps(rate_list), status=200)
  elif request.method=='GET':
    if full_path is None or full_path == '':
      return Response('There are no available files', status=404)
    try:
      return send_file(filename_or_fp=full_path,mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',cache_timeout=0,as_attachment=True)
    except FileNotFoundError as e:
      return Response(str(e), status=404)  
        
