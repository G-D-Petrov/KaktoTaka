import requests
import json
import ast 

r = requests.get('https://tus5jpx6z6.execute-api.eu-central-1.amazonaws.com/dev', data=json.dumps({"SensorType": "distance","top": 10}))
json_new = json.loads(r.text)
# resp = r.text.replace("\\", "")
data = ast.literal_eval(json_new['body'])
for line in data:
  print(line)
print( )