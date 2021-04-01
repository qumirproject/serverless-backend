import json
import boto3
from datetime import date

def getNow(mask = "%Y%m%d"):
    today = date.today()

    # dd/mm/YY
    return today.strftime(mask)

def setGardenerInfo(event):
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
    firstname = params['firstname']
    lastname = params['lastname']

    # there's 2 option. A new entry or an update for an existing one
    if mode == 'new':
        # create a new gardener
        query = {
            "TableName": "gardeners",
            "Item": {
                "user_id": {"S":usr_id}, 
                "firstname": {"S":firstname}, 
                "lastname": {"S":lastname}, 
                "activation_date": {"S":getNow()}
            }
        }
        ddb.put_item(**query)
    else:
        # update gardener's profile
        query = {
            "TableName": "gardeners",
            "Key": {
                "user_id": {"S":usr_id}
            },
            "UpdateExpression": "SET #8edd0 = :8edd0, #8edd1 = :8edd1",
            "ExpressionAttributeNames": {"#8edd0":"firstname","#8edd1":"lastname"},
            "ExpressionAttributeValues": {":8edd0": {"S":firstname},":8edd1": {"S":lastname}}
        }
        ddb.update_item(**query)

def lambda_handler(event, context):
    try:
        setGardenerInfo(event)

        return {
            'statusCode': 200,
            'headers' : {
                'Access-Control-Allow-Headers' : 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,QUMIR-TOKEN'
                ,'Access-Control-Allow-Methods' : 'POST,OPTIONS'
                ,'Access-Control-Allow-Origin' : '*'
                #,'Access-Control-Allow-Credentials' : 'true'
            }
        }
    except BaseException as error:
        #print("Unknown error while putting item: " + error.response['Error']['Message'])
        print(error)
        return {
            'statusCode': 400,
            'headers' : {
                'Access-Control-Allow-Headers' : 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,QUMIR-TOKEN'
                ,'Access-Control-Allow-Methods' : 'POST,OPTIONS'
                ,'Access-Control-Allow-Origin' : '*'
                #,'Access-Control-Allow-Credentials' : 'true'
            }
        }