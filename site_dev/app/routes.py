from app import app
from flask import render_template

@app.route("/")
@app.route("/home")
def index():
  area_labels = ["January","February","March","April","May","June","July","August"]
  area_data = [10,9,8,7,6,4,7,8]
  context = {
    "area_labels": area_labels,
    "area_data": area_data,
    "monthly_earnings": "50000",
    "annual_earnings": "500000",
    "data_usage": "75",
    "sales_requests": "14",
  }
  return render_template('index.html', context=context)