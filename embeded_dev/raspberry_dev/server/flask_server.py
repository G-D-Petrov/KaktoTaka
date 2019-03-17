#/usr/bin/python

from flask import Flask
from flask import request
from datetime import datetime
import json
import requests


app = Flask(__name__)

print("Aideeeee")

def process_message(message):
    id_zero = '00'
    id_one  = '01'
    id_two  = '02'
    elements = message.split('|')
    
    temperature_measurment = '00'
    light_measurment       = '01'
    distance_measurment    = '02'
    humidity_measurment    = '03'
    lpg_measurment         = '04'
    co_measurment          = '05'
    smoke_measurment       = '06'    

    
    time_mes = str(datetime.now())
    device_id = elements[1]
    sensor_id = elements[2]
    sensor_value = elements[3]
    sesnsor_type = 'unknown'
    
    if temperature_measurment == sensor_id:
        sesnsor_type = 'tempreture'
    elif light_measurment      == sensor_id:
        sesnsor_type = 'light'
    elif distance_measurment == sensor_id:
        sesnsor_type = 'distance'
    elif humidity_measurment == sensor_id:
        sesnsor_type = 'humidity'
    elif lpg_measurment == sensor_id:
        sesnsor_type = 'lpg'
    elif co_measurment == sensor_id:
        sesnsor_type = 'co'
    elif smoke_measurment == sensor_id:
        sesnsor_type = 'smoke'
    
    json_to_zdravko = json.dumps({'UserId': 'Pesho', 'SensorId': sensor_id, 'SensorType': sesnsor_type, 'Readings': sensor_value.strip(), 'TimeStamp': time_mes})
    print('Json to zdravko:')
    print(json_to_zdravko)
    try:
        r = requests.post('https://tus5jpx6z6.execute-api.eu-central-1.amazonaws.com/dev', data=json_to_zdravko)
    except Exception as e:
        print(e)
    print('Successful post!!!!')
    print(r.text)


@app.route('/', methods=["GET", "POST"])
def hello_world():
    if not 'Data' in request.form.keys():
        print("Vincent pak obyrka neshto!!!!!")
        return 'Begai!!!'
    else:
        data=request.form['Data']
        print("Data:")
        print(data)
        
        process_message(data)
        return 'Hello, World!'

app.run(host='0.0.0.0')