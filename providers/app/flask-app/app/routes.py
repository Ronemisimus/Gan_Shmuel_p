import requests, json
from flask import request, jsonify, Response, json, redirect, url_for, send_file
from app import app, db
from app.models import Truck, Provider, Rate
from datetime import datetime, timezone
import xlrd, os

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
      try:
        res = requests.get(item_url, data={'from': from_date, 'to': to_date})
        res = json.dumps(res.json())
      except Exception as e:
        return Response(str(e))

      return Response(res, mimetype='application/json')

@app.route('/bill/<id>')
def getBill(id):
  provider_id=Provider.query.filter_by(id=id).first()
  if provider_id is None:
    return Response(json.dumps('Provider ({}) Not Found'.format(id)),mimetype='application/json')
  else:
    provider_name=Provider.query.filter_by(id=id)
    product_amount = {}
    product_session_count = {}
    products_list=[]
    truck_count=0
    session_count=0
    from_date=request.args.get('from')
    to_param=request.args.get('to')
    to_date = datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S') if to_param is None else to_param
    trucks_of_provider=Truck.query.filter_by(provider_id=id).all()
    print(type(trucks_of_provider))
    for truck in trucks_of_provider:
      truck_count+=1
      res=request.get('http://localhost:8086/truck/'+truck, data ={'from':from_date ,'to':to_date})
    # { 
    # "id": <str>,
	  # "tara": <int>, // last known tara in kg
	  # "sessions": [ <id1>,...] 
    #     }
      for session in res['sessions']:
        session_count+=1
        res_session=request.get('http://18.194.232.207:8088/session/'+session)
        # method get session id and return json in format:
    # [{
    # 	"id": "<id>",
    # 	"truckID": "<truck id>",
    # 	"items":
    #  [{
    # 		"produce": "<type of produce>",
    # 		"bruto": "<weight bruto>",
    # 		"neto": "<weight_neto| null>"
    # 	}]
    # }]
        for product in res_session['items']:
          if product['produce'] in product_session_count:
            product_session_count[product['produce']]+=1
          else:
            product_session_count[product['produce']]=1
          if product in product_amount:
            product_amount[product['produce']]+=product['neto']
          else:
            product_amount[product['produce']]=product_amount[product['produce']]

  #  {
	#   "id": <str>,
	#   "name": <str>,
	#   "from": <str>,
	#   "to": <str>,
	#   "truckCount": <int>,
	#   "sessionCount": <int>,
	#   "products": [
	#     { "product":<str>,
	#       "count": <str>, // number of sessions
	#       "amount": <int>, // total kg
	#       "rate": <int>, // agorot
	#       "pay": <int> // agorot
	#     },...
	#   ],
	#   "total": <int> // agorot
	# }
    total_pay=0
    for key in product_session_count:
      if Rate.query.filter_by(product_id=key , scope=id) is None:
        rate=Rate.query.filter_by(product_id=key , scope=id)
      else:
        rate=Rate.query.filter_by(product_id=key , scope='ALL').first()
      product_details={'product':key ,'count':product_session_count[key],'amount':product_amount[key],'rate':rate,'pay':(rate*product_amount[key])}
      total_pay+=product_details['pay']
      products_list.append(product_details)
    res_data = {'ID':id ,
    'Name':provider_name,
    'From':from_date,
    'To':to_date,
    'Truck_count':truck_count,
    'Session_Count':session_count,
    'Products':products_list,
    'Total':total_pay}
  return Response(json.dumps(res_data),mimetype='application/json')



@app.route('/rates', methods=['GET' , 'POST'])
def rates():
    global filename, full_path
    if request.method=='POST':
      try:
        filename=request.form['file']
      except:
        return "No file name was given. Please mention wanted file's name inside the form."
      finally:
        full_path=os.getcwd()+'/in/'+filename+'.xlsx'
        print(full_path)
      try:
        book = xlrd.open_workbook(full_path, on_demand=True)
      except:
          print ("File doesn't exists in '/in' folder.") #ToDo - insert to a logger
          return Response(status=404)
      else: ## Case file was opend successfuly
        sheet = book.sheet_by_index(0) ## ToDo: change to find sheet by name
        for i in range(1,sheet.nrows):
          for j in range(sheet.ncols):
            if j==0:
              product=str(sheet.cell(i,j).value )
            elif j==1:
              rate = int(sheet.cell(i,j).value )
            elif j==2:
              scope = str(sheet.cell(i,j).value )
          new_rate_candidate=Rate.query.filter_by(product_id=product, scope=scope).first()
          if new_rate_candidate is None:
            new_rate = Rate(product_id=product,rate=rate,scope=scope)
            try:
              db.session.add(new_rate)
              db.session.commit()
            except:
              print ("Coldn't insert data to billdb.table 'Rates'")
              return Response(status=500)
          else:
            new_rate_candidate.rate=rate
            db.session.commit()

        book.release_resources()
        return 'Done'

    elif request.method=='GET':
      print("in get "+full_path)
      try:
        print("trying to retraive "+full_path)
        return send_file(filename_or_fp=full_path,mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',cache_timeout=0,as_attachment=True)
      except FileNotFoundError:
        return Response(status=404)  
        
