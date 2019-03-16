from app import app
import requests
import json
import ast 
from flask import render_template, session, redirect, request, url_for

def get_data():
  r = requests.get('https://tus5jpx6z6.execute-api.eu-central-1.amazonaws.com/dev', data=json.dumps({"SensorType": "distance","top": 100}), timeout=30)
  json_new = json.loads(r.text)
  data = ast.literal_eval(json_new['body'])
  count = 0
  labels_out = []
  data_out = []
  for line in data:
    count += 1
    labels_out.append(count)
    data_out.append(line[3])

  return labels_out, data_out


@app.route("/")
@app.route("/home")
def index():
  if 'user' not in session:
    return redirect(url_for('login'))

  if not session['user']:
    return redirect('/login')
  area_labels = ["January","February","March","April","May","June","July","August"]
  area_data = [10,9,8,7,6,4,7,8]
  area_labels, area_data = get_data()
  print(session['user'])
  context = {
    "area_labels": area_labels,
    "area_data": area_data,
    "monthly_earnings": "50000",
    "annual_earnings": "500000",
    "data_usage": "75",
    "sales_requests": "14",
    "label": "Distance Measurments",
    "username": session['user']
  }
  return render_template('index.html', context=context)

@app.route('/login', methods=['GET', 'POST'])
def login():
  if 'user' in session:
    if session['user'] is not None and session['user'] != "":
      return redirect('/')
  print(request.method)
  if request.method == 'POST':
    session['user'] = request.form['username']
    return redirect('/')
  return render_template('login.html')