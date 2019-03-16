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

def getSqlSelect(top, filters):
    selectQuery = "select * from SensorData"
    if len(filters) != 0:
        selectQuery += " WHERE "
        selectQuery += " " + filters[0][0] + "='" + filters[0][1] + "'"
        
        for i in range(1, len(filters)):
            selectQuery += " AND " + filters[i][0] + "='" + filters[i][1] + "'"

    if top != 0:
        selectQuery += " LIMIT " + str(top)

    return selectQuery


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
    top = 0
    filters = list()
    
    if 'top' in event:
        top = event['top']
    if 'SensorType' in event:
        filters.append(('SensorType', event['SensorType']))
    if 'UserId' in event:
        filters.append(('UserId', event['UserId']))
        
    with conn.cursor() as cur:
        #cur.execute("""select * from SensorData""")
        sqlSelect = getSqlSelect(top, filters)
        print("SqlSelect: " + sqlSelect)
        cur.execute(sqlSelect)
        conn.commit()
        cur.close()
        for row in cur:
            temp_list = list(row)
            curLine = temp_list[:-1]
            curLine.append(str(temp_list[-1]))
            result.append(curLine)
        print("Data from RDS...")
        print(result)
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
