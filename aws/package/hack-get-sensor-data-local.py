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

    """
    This function fetches content from mysql RDS instance
    """
    result = []
    print("Before connection!")
    conn = pymysql.connect(rds_host, port=3306, user=name, passwd=password, db=db_name, connect_timeout=2)
    print("Connected!")
    with conn.cursor() as cur:
        cur.execute("""select * from SensorData""")
        conn.commit()
        cur.close()
        for row in cur:
            result.append(list(row))
        print("Data from RDS...")
        print(result)
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Data has been gotten successfuly!')
    }
