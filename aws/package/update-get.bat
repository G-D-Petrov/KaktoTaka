zip -g function.zip hack-get-sensor-data-local.py && aws lambda update-function-code --function-name hack-get-sensor-data --zip-file fileb://function.zip