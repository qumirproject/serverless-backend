import json
import boto3

def getGardenerInfo(event):
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

    # Ask for the gardeners info. Maybe it's his/her first time here!
    query =  {
        "TableName": "gardeners",
        "Key": {
            "user_id": {"S":usr_id}
        }
    }
    ans = ddb.get_item(**query)
    gardener_item = ans.get('Item', None)
    if gardener_item:
        out_res = 'OK'

        # Go for the gardens info
        query = {
            "TableName": "gardens",
            "KeyConditionExpression": "#ea440 = :ea440",
            "ExpressionAttributeNames": {"#ea440":"gardener_id"},
            "ExpressionAttributeValues": {":ea440": {"S":usr_id}}
        }
        ans = ddb.query(**query)
        print('hola')
        print(ans)
        gardens_item = ans.get('Items', None)

    else:
        out_res = 'USRCRT'
        gardens_item = None

    return {
        'out_res': out_res,
        'gardener_info' : gardener_item,
        'gardens_info' : gardens_item
    }


def lambda_handler(event, context):
    try:
        gardenerinfo = getGardenerInfo(event)
        return {
            'statusCode': 200,
            'headers' : {
                'Access-Control-Allow-Headers' : 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,QUMIR-TOKEN'
                ,'Access-Control-Allow-Methods' : 'GET,OPTIONS'
                ,'Access-Control-Allow-Origin' : '*'
                #,'Access-Control-Allow-Credentials' : 'true'
            },
            'body': json.dumps(gardenerinfo)
            #'body' : json.dumps(ans)
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