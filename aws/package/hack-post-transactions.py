import json
import boto3
import pymysql
import sys
from datetime import datetime
import math

client = boto3.client('dynamodb')
rds_host = "ocado-hackathon-2.cmftyvsmwhn6.eu-central-1.rds.amazonaws.com"
name = "admin"
password = "adminadmin"
db_name = "TheBigDatabase"

def getSensorUnitCost(cur, SensorType):
    query = "select UnitCost from SensorCost where SensorType='{}';".format(SensorType)
    
    cur.execute(query)
    row = cur.fetchone()
    unitCost = float(row[0])
    
    return unitCost

def doesUserHaveEnoughMoney(cur, UserId, neededMoney):
    query = "select COUNT(*) from User where UserId='{}' and parichki>{};".format(UserId, neededMoney)
    
    print("doesUserHaveEnoughMoney(): " + query)

    cur.execute(query)
    row = cur.fetchone()
    result = int(row[0]) == 1
    
    return result

def getSystemHasEnoughData(cur, SensorType, NumberOfData):
    query = "SELECT COUNT(*) FROM SensorData where SensorType='{}';".format(SensorType)
    
    cur.execute(query)
    row = cur.fetchone()
    systemHasEnoughData = int(row[0])
    
    return systemHasEnoughData
    

def check_prerequesits(event, cur, sensorUnitCost):
    ## Does user have enough money?
    userHasMoney = doesUserHaveEnoughMoney(cur, event["UserId"], sensorUnitCost * event["NumberOfData"])
    print("User has money: " + str(userHasMoney))
    if not userHasMoney:
        return { 'statusCode': 304, 'body': json.dumps('User doesnt have enough money') }
    
    ## Does the table have enough sensor data as requested?
    systemHasEnoughData = getSystemHasEnoughData(cur, event['SensorType'], event['NumberOfData'])
    print("System has enough data: " + str(systemHasEnoughData))
    if not systemHasEnoughData:
        return { 'statusCode': 305, 'body': json.dumps('System does not have enough data') }
        
    return None
    
def getNumberOfUserHavingSensor(cur, SensorType):
    query = "select count(*) from (SELECT COUNT(*) from SensorData where SensorType='{}' group by UserId) t;".format(SensorType)
    
    cur.execute(query)
    row = cur.fetchone()
    result = int(row[0])
    
    return result
    

def getNumberOfUsersWithAmount(cur, SensorType, equal_amount):
    query = "SELECT COUNT(*) from SensorData where SensorType='{}' group By SensorType, UserId;".format(SensorType)
    
    cur.execute(query)
    rows = cur.fetchall()
    numberOfMatches = 0
    for row in rows:
        if int(row[0]) > equal_amount:
            numberOfMatches += 1
    
    return numberOfMatches


def decreaseBuyerCost(cur, UserId, transactionCost):
    query = "UPDATE User SET Parichki=Parichki-{} WHERE UserId='{}';".format(transactionCost, UserId)
    cur.execute(query)

def increaseSellersCost(cur, SensorType, equal_amount):
    print("increaseSellersCost()")
    query = """UPDATE User 
            SET Parichki = Parichki + {} 
            WHERE UserId IN (
                select distinct UserId
                from SensorData
                where SensorType = '{}'
                );""".format(equal_amount, SensorType)
    cur.execute(query)
    
    query = """select distinct UserId
                from SensorData
                where SensorType = '{}';""".format(SensorType)
    cur.execute(query)
    users = cur.fetchall();
    result = list()
    for user in users:
        result.append(user[0])
    print(result)
    return result

def addTransaction(cur, UserId, SensorType, NumberOfData):
    query = "insert into Transaction Values('{}', '{}', {});".format(UserId, SensorType, NumberOfData)
    cur.execute(query)

def make_equal_transaction(event, cur, SensorType, transactionCost, equal_amount):
    print('make_equal_transaction')
    # decrease buyer parichki
    decreaseBuyerCost(cur, event['UserId'], transactionCost)
    # increase sellers parichki
    users = increaseSellersCost(cur, SensorType, equal_amount)
    # add transaction to table
    addTransaction(cur, event['UserId'], SensorType, event['NumberOfData'])
    
    return users

# increase sellers parichki
def increaseSellerCost(cur, maxSellerUser, transactionCost):
    query = """UPDATE User SET Parichki=Parichki+{} WHERE UserId='{}'""".format(transactionCost, maxSellerUser)
    cur.execute(query)

def make_max_transaction(event, cur, SensorType, transactionCost, NumberOfData):
    print('make_max_transaction')
    query = """SELECT UserId, COUNT(*) as C
            FROM SensorData
            WHERE SensorType='{}'
            GROUP BY UserId
            ORDER BY C DESC
            LIMIT 1;""".format(SensorType)
    cur.execute(query)
    row = cur.fetchone()
    maxSellerUser = row[0]
    userSensorDataCount = int(row[1])
    if userSensorDataCount < NumberOfData:
        return (None, {
            'statusCode': 306,
            'body': json.dumps('Even the user with maximum data does not have the required number of data! Please ask for less data!')
        })
    
    # decrease buyer parichki
    decreaseBuyerCost(cur, event['UserId'], transactionCost)
    # increase sellers parichki
    increaseSellerCost(cur, maxSellerUser, transactionCost)
    # add transaction to table
    addTransaction(cur, event['UserId'], SensorType, event['NumberOfData'])

    print([maxSellerUser])
    return ([maxSellerUser], None)

def getResultData(cur, users, NumberOfData):
    print("getResultData()")
    userTuple = tuple(users)
    query = ""
    if len(userTuple) == 1:
        query = """select SensorReadings 
            from SensorData
            where UserId in ('{}')
            order by TimeStamp desc
            limit {};""".format(str(userTuple[0]), NumberOfData)
    else:
        query = """select SensorReadings 
            from SensorData
            where UserId in {}
            order by TimeStamp desc
            limit {};""".format(str(userTuple), NumberOfData)
    print(query)
    cur.execute(query)
    rows = cur.fetchall()
    
    result = list()
    for row in rows:
        result.append(row[0])
    
    print(result)
    return result

def make_transaction(event, cur, transactionCost):
    numberOfUsersHavingSensor = getNumberOfUserHavingSensor(cur, event['SensorType'])
    print("Number of users having sensor: " + str(numberOfUsersHavingSensor))
    equal_amount = transactionCost / numberOfUsersHavingSensor
    equal_number_of_data = event['NumberOfData'] / numberOfUsersHavingSensor
    print("Equal amount is: " + str(equal_amount))
    numberOfUsersWithEqualNumberOfData = getNumberOfUsersWithAmount(cur, event['SensorType'], equal_number_of_data)
    print("Number of users having sensor: " + str(numberOfUsersWithEqualNumberOfData))
    
    result_data = list()
    users = list()
    if numberOfUsersHavingSensor == numberOfUsersWithEqualNumberOfData:
        users = make_equal_transaction(event, cur, event['SensorType'], transactionCost, equal_amount)
    else:
        (users, max_trans_error) = make_max_transaction(event, cur, event['SensorType'], transactionCost, event['NumberOfData'])
        if max_trans_error is not None:
            return (None, max_trans_error)
    
    
    result_data = getResultData(cur, users, event['NumberOfData'])    
    
    return (result_data, None)

def lambda_handler(event, context):

    # Get the current date and time in yy--mm-dd hours:minutes:second format

    """
    This function fetches content from mysql RDS instance
    """
    result = []
    print("Before connection!")
    conn = pymysql.connect(rds_host, port=3306, user=name, passwd=password, db=db_name, connect_timeout=2)
    print("Connected!")
    
    print(event.keys());
    if ("UserId" not in event.keys()) or ("SensorType" not in event.keys()) or ("NumberOfData" not in event.keys()):
        return {
            'statusCode': 303,
            'body': json.dumps('Bad request, Gergi! Some of the values were not specified: UserId, SensorType, NumberOfData')
        }
    
    # event => { "UserId": "Daniela", "SensorType": "co", "NumberOfData": 20 }
    
    result_data = list()
    with conn.cursor() as cur:
        sensorUnitCost = getSensorUnitCost(cur, event['SensorType'])
        print("UnitCost is: " + str(sensorUnitCost))
        
        prerequesits_error = check_prerequesits(event, cur, sensorUnitCost)
        if prerequesits_error is not None:
            return prerequesits_error

        ## Get number of users having this SensorType, if all of them have NumberOfData/3 => OK, take from all. Else if the gratest has at least NumberOfData, take them. Else exception.
        (result_data, transaction_error) = make_transaction(event, cur, sensorUnitCost * event["NumberOfData"])
        if transaction_error is not None:
            return transaction_error
        
        conn.commit()
        cur.close()
    
    print(result_data)
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps(str(result_data))
    }
