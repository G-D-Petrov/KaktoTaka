import serial
import psycopg2
from creds import creds

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
    id_zero = '#00'
    id_one  = '#01'
    if(message.find(id_zero) is not -1):
        message = message.replace(id_zero, '')
        print('Device 00 ')
        extract_value(message)
    elif(message.find(id_one) is not -1):
        message = message.replace(id_one, '')
        print('Device 01 ')
        extract_value(message)
    
    

# serZero = serial.Serial('/dev/ttyUSB0', 9600)
# serOne = serial.Serial('/dev/ttyUSB1', 9600)

# while 1:
#     if(serZero.inWaiting()> 0):
#         line = serZero.readline()
#         process_message(line)
#         ##print(line)
#     if(serOne.inWaiting()> 0):
#         line = serOne.readline()
#         process_message(line)
        
conn_string = "host="+ creds.PGHOST +" port="+ "5432" +" dbname="+ creds.PGDATABASE +" user=" + creds.PGUSER \
+" password="+ creds.PGPASSWORD
conn=psycopg2.connect(conn_string)
print("Connected!")
        