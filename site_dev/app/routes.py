from app import app
import requests
import json
import ast 
from flask import render_template, session, redirect, request, url_for

def get_user_data():
  r = requests.get('https://tus5jpx6z6.execute-api.eu-central-1.amazonaws.com/dev', data=json.dumps({"UserId": session['user']}), timeout=30)
  json_new = json.loads(r.text)
  data = ast.literal_eval(json_new['body'])
  count = 0
  data_dict = {}
  labels_out = []
  data_out = []
  for line in data:
    count += 1
    if line[2] not in data_dict:
      data_dict[line[2]] = 1
    else:
      data_dict[line[2]] += 1

  return data_dict.keys(), data_dict.values()

def get_home():
  if 'user' not in session:
    return redirect(url_for('login'))

  if not session['user']:
    return redirect('/login')
  area_labels = ["January","February","March","April","May","June","July","August"]
  area_data = [10,9,8,7,6,4,7,8]
  pie_labels, pie_data = get_user_data()

  context = {
    "area_labels": area_labels,
    "area_data": area_data,
    "pie_labels": pie_labels,
    "pie_data": pie_data,
    "monthly_earnings": "50000",
    "annual_earnings": "500000",
    "data_usage": "75",
    "sales_requests": "14",
    "label": "Distance Measurments",
    "username": session['user']
  }

  return context

def post_home():
  json_to_zdravko = {
    "UserId": session['user'],
    "SensorType": request.form['sensorType'],
    "NumberOfData": int(request.form['amount'])
  }
  r = requests.post('https://tus5jpx6z6.execute-api.eu-central-1.amazonaws.com/dev/transactions', data=json.dumps(json_to_zdravko))

  json_new = json.loads(r.text)
  data = ast.literal_eval(json_new['body'])
  new_data = []
  labels = []
  count = 0
  print(r.text)
  for d in ast.literal_eval(data):
    count += 1
    labels.append(count)
    new_data.append(d)

  return labels, new_data


@app.route("/", methods=['GET', 'POST'])
def index():
  context = get_home()
  if request.method == 'POST':
    context['area_labels'], context['area_data'] = post_home()
  
  return render_template('index.html', context=context)


@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    session['user'] = request.form['username']
    return redirect('/')
  return render_template('login.html')