import json
import boto3
import pymysql
import sys


client = boto3.client('dynamodb')
rds_host = "ocado-hackathon-2.cmftyvsmwhn6.eu-central-1.rds.amazonaws.com"
name = "admin"
password = "adminadmin"
db_name = "TheBigDatabase"


def save_data(event):
    """
    This function fetches content from mysql RDS instance
    """
    result = []
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
    with conn.cursor() as cur:
        cur.execute("""insert into SensorData (UserId, SensorId , SensorType , SensorReadings) values( %s, '%s', %s, %s)""" % (event['UserId'], event['SensorId'], event['SensorType'] , event['Readings']))
        #cur.execute("""select * from test""")
        conn.commit()
        cur.close()
        # for row in cur:
        #     result.append(list(row))
        # print "Data from RDS..."
        # print result


def lambda_handler(event, context):

    # Get the current date and time in yy--mm-dd hours:minutes:second format
    now = datetime.now()
    now_str = now.strftime('%Y-%m-%d %H:%M:%S')    

    save_data(event)
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Data has been posted successfuly!')
    }
