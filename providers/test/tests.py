import requests, os, sys, json
from datetime import datetime, timezone


test_url = os.environ['TEST_URL']
test_port = os.environ['PORT']
url = '{}:{}'.format(test_url, test_port)
log_file = '.log'
is_error = False

new_truck = {'id':'214-63-807', 'provider_id': 10001}
provider = {'name':'pro2', 'id':10002}
new_rate = {'product_id':'test product','rate':100,'scope':'ALL'}
new_rate_pro = {'product_id':'test product','rate':100,'scope':'pro1'}
get_truck_data = {'id': 'Truck1', 'from': 20200202112732, 'to': 20211231011500}
get_truck_res = {"id":"Truck1","sessions":[35],"tara":92}
post_provider='Itzik'
put_provider={'id':10001,'name':"Moshe"}
get_bill_id={'id':10001,'from': 20200202112732, 'to': 20211231011500}

def log_error_msg(msg, error):
  naive_date = datetime.now(timezone.utc)
  date_str = naive_date.strftime('%x %H:%M:%S')
  error_msg = '[Matan]-[{}] - {}:\n {}\n'.format(date_str, msg, error)
  print(error_msg)
  with open(log_file, 'a+') as log:
    log.write(error_msg)
  return

def test_health():
  global is_error
  try:
    requests.get('{}/health'.format(url))
  except Exception as e:
    is_error = True
    log_error_msg('DB connection failed', e)
def test_provider_post():
  global is_error
  global post_provider
  try:
    requests.post('{}/provider'.format(url),data={'provider':post_provider})
  except Exception as e:
    is_error = True
    log_error_msg('Insert New provider failed', e)
  return
def tset_provider_put():
  global is_error
  global put_provider
  try:
    requests.put('{}/provider/{}'.format(url,put_provider['id']),data={'provider_name':put_provider['name']})
  except Exception as e:
    is_error = True
    log_error_msg('Insert New truck failed', e)
  return

def test_post_truck():
  global new_truck
  global is_error
  try:
    res = requests.post('{}/truck'.format(url), data={'provider_id': new_truck['provider_id'], 'truck': new_truck['id']})
    res = json.dumps(res.json())
  except Exception as e:
    is_error = True
    log_error_msg('Insert New truck failed', e)
  else:
    expected_res = json.dumps(new_truck)
    is_error = not (expected_res == res)
  return

def test_update_truck():
  global new_truck
  global is_error
  try:
    res = requests.put('{}/truck/{}'.format(url, new_truck['id']), data={'provider_id': provider['id']})
    res = json.dumps(res.json())
  except Exception as e:
    is_error = True
    log_error_msg('Update truck failed', e)
  else:
    expected_res = json.dumps({'id': new_truck['id'], 'provider_id': provider['id']})
    is_error = not (expected_res == res)
  return

def test_get_truck():
  global new_truck
  global is_error
  try:
    res = requests.get('{}/truck/{}?from={}&to={}'.format(url, get_truck_data['id'], get_truck_data['from'], get_truck_data['to']))
    res = json.dumps(res.json())
  except Exception as e:
    is_error = True
    log_error_msg('GET truck failed', e)
  else:
    expected_res = json.dumps(get_truck_res)
    is_error = not (expected_res == res)
  return

  def test_get_bill():
    global get_bill_id
    global is_error
    try:
      requests.get('{}/bill/{}?from={}&to={}'.format(url,get_bill_id['id'],get_bill_id['from'],get_bill_id['to']))
    except Exception as e:
      is_error = True
      log_error_msg('Trying to get bill for provider failed', e)
    return


test_health()
test_post_truck()
test_update_truck()
test_get_truck()
test_provider_post()
tset_provider_put()
test_get_bill()

if is_error:
  print('Error!!')
else:
  print(0)