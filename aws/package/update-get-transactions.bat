zip -g function.zip hack-get-transcations.py && aws lambda update-function-code --function-name hack-get-transcations --zip-file fileb://function.zip