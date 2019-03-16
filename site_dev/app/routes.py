from app import app
import requests
import json
import ast 
from flask import render_template

def get_data():
  r = requests.get('https://tus5jpx6z6.execute-api.eu-central-1.amazonaws.com/dev', data=json.dumps({"SensorType": "distance","top": 10}))
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
  r = requests.get('https://tus5jpx6z6.execute-api.eu-central-1.amazonaws.com/dev')
  print(r.text)
  area_labels = ["January","February","March","April","May","June","July","August"]
  area_data = [10,9,8,7,6,4,7,8]
  area_labels, area_data = get_data()
  context = {
    "area_labels": area_labels,
    "area_data": area_data,
    "monthly_earnings": "50000",
    "annual_earnings": "500000",
    "data_usage": "75",
    "sales_requests": "14",
  }
  return render_template('index.html', context=context)