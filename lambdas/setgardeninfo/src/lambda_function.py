import json
import boto3
from datetime import date
import random
import string

def getNow(mask = "%Y%m%d"):
    today = date.today()

    # dd/mm/YY
    return today.strftime(mask)

def generateGardenId(len = 16):
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(len))

def setGardenInfo(event):
    params = event['queryStringParameters']
    usr_id = event['requestContext']['authorizer']['claims']['cognito:username']
    try:
        enviroment = params['env']
    except:
        enviroment = 'dev'
    
    # Choosing enviroment. Production (online) or Development (localhost)
    if enviroment == 'dev':
        ddb = boto3.client("dynamodb",
                            endpoint_url="http://localhost:8000",
                            aws_access_key_id="vmnu1",
                            aws_secret_access_key="z7m86")
    else:
        ddb = boto3.client("dynamodb")

    # Specific parameters
    mode = params['mode']
    garden_type = params['type']
    garden_descr = params['description']
    now = getNow()
    gardenid = generateGardenId()

    # there's 2 option. A new entry or an update for an existing one
    if mode == 'new':
        # create a new garden with a new ID
        query = {
            "TableName": "gardens",
            "Item": {
                "garden_id": {"S":gardenid}, 
                "gardener_id": {"S":usr_id}, 
                "type": {"S":garden_type}, 
                "description": {"S":garden_descr}, 
                "creation_date": {"S":now}
            }
        }
        ddb.put_item(**query)
    else:
        # update garden's info
        gardenid = params['garden_id']
        query = {
            "TableName": "gardens",
            "Key": {
                "garden_id": {"S":gardenid}, 
                "gardener_id": {"S":usr_id}
            },
            "UpdateExpression": "SET #4b830 = :4b830, #4b831 = :4b831",
            "ExpressionAttributeNames": {"#4b830":"type","#4b831":"description"},
            "ExpressionAttributeValues": {":4b830": {"S":garden_type},":4b831": {"S":garden_descr}}
        }
        ddb.update_item(**query)

def lambda_handler(event, context):
    try:
        setGardenInfo(event)

        return {
            'statusCode': 200,
            'headers' : {
                'Access-Control-Allow-Headers' : 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,QUMIR-TOKEN'
                ,'Access-Control-Allow-Methods' : 'GET,OPTIONS'
                ,'Access-Control-Allow-Origin' : '*'
                #,'Access-Control-Allow-Credentials' : 'true'
            },
            'body': None
        }
    except BaseException as error:
        #print("Unknown error while putting item: " + error.response['Error']['Message'])
        print(error)
        return {
            'statusCode': 400,
            'headers' : {
                'Access-Control-Allow-Headers' : 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,QUMIR-TOKEN'
                ,'Access-Control-Allow-Methods' : 'GET,OPTIONS'
                ,'Access-Control-Allow-Origin' : '*'
                #,'Access-Control-Allow-Credentials' : 'true'
            },
            'body': None
        }