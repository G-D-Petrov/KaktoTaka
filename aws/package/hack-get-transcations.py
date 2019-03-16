import json
import boto3
import pymysql
import sys
from datetime import datetime

client = boto3.client('dynamodb')
rds_host = "ocado-hackathon-2.cmftyvsmwhn6.eu-central-1.rds.amazonaws.com"
name = "admin"
password = "adminadmin"
db_name = "TheBigDatabase"


def lambda_handler(event, context):

    # Get the current date and time in yy--mm-dd hours:minutes:second format
    now = datetime.now()
    now_str = now.strftime('%Y-%m-%d %H:%M:%S')
    print(now_str)
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps("Zdravei bat gergi, dobre doshul pri tranzakciite!!!")
    }
