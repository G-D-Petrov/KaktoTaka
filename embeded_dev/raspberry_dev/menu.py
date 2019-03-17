import serial
import json
import requests
from datetime import datetime


def extract_value(message):
    temperature_measurment = '%00&'
    light_measurment       = '%01&'
    distance_measurment    = '%02&'
    humidity_measurment    = '%03&'
    lpg_measurment         = '%04&'
    co_measurment          = '%05&'
    smoke_measurment       = '%06&'    
    if(message.find(temperature_measurment) is not -1):
        message = message.replace(temperature_measurment, '')
        print('Temperature: ')
        print(message)
        print('\n')
    elif(message.find(light_measurment) is not -1):
        message = message.replace(light_measurment, '')        
        print('Light: ')
        print(message)
        print('\n')
    elif(message.find(distance_measurment) is not -1):
        message = message.replace(distance_measurment, '')        
        print('Distance: ')
        print(message)
        print('\n')
    elif(message.find(humidity_measurment) is not -1):
        message = message.replace(humidity_measurment, '')        
        print('Humidity: ')
        print(message)
        print('\n')
    elif(message.find(lpg_measurment) is not -1):
        message = message.replace(lpg_measurment, '')        
        print('LPG: ')
        print(message)
        print('\n')
    elif(message.find(co_measurment) is not -1):
        message = message.replace(co_measurment, '')        
        print('CO: ')
        print(message)
        print('\n')
    elif(message.find(smoke_measurment) is not -1):
        message = message.replace(smoke_measurment, '')        
        print('Smoke: ')
        print(message)
        print('\n')

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
    
    
    json_to_zdravko = json.dumps({'UserId': 'Daniela', 'SensorId': sensor_id, 'SensorType': sesnsor_type, 'Readings': sensor_value.strip(), 'TimeStamp': time_mes})
    print(json_to_zdravko)
    r = requests.post('https://tus5jpx6z6.execute-api.eu-central-1.amazonaws.com/dev', data=json_to_zdravko)
    print(r.text)
    """
    if(message.find(id_zero) is not -1):
        message = message.replace(id_zero, '')
        print('Device 00 ')
        extract_value(message)
    elif(message.find(id_one) is not -1):
        message = message.replace(id_one, '')
        print('Device 01 ')
        extract_value(message)
    """
    

serZero = serial.Serial('/dev/ttyUSB0', 9600)
serOne = serial.Serial('/dev/ttyUSB1', 9600)

while 1:
    if(serZero.inWaiting()> 0):
        line = serZero.readline()
        process_message(line)
        ##print(line)
    if(serOne.inWaiting()> 0):
        line = serOne.readline()
        process_message(line)
        
        
        