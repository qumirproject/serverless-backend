import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    http_method = event['httpMethod']
    params = event['queryStringParameters']
    usr_id = event['requestContext']['authorizer']['claims']['cognito:username']
    try:
        enviroment = params['env']
    except:
        enviroment = 'dev'
    #print("Received event: " + json.dumps(event, indent=4))
    print(http_method)
    print(params)
    print(usr_id)
    print(enviroment)
    print('COMIENZA AQUÍ LA SECCIÓN DYNAMODB')
    ddb = boto3.client("dynamodb",
                        endpoint_url="http://localhost:8000",
                        aws_access_key_id="vmnu1",
                        aws_secret_access_key="z7m86")
    
    gardener = {
        "TableName": "gardeners",
        "Item": {
            "user_id": {"S":"matiastorresrisso"}, 
            "activation_date": {"S":"20210121"}, 
            "firstname": {"S":"Matías"}, 
            "lastname": {"S":"Torres"}
        }
    }
    #ddb.put_item(**gardener)
    print(ddb.list_tables())

    print('FINALIZA AQUÍ LA SECCIÓN DYNAMODB')
    return {
        'statusCode': 200,
        'headers' : {
            'Access-Control-Allow-Headers' : 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,QUMIR-TOKEN'
            ,'Access-Control-Allow-Methods' : 'GET,OPTIONS'
            ,'Access-Control-Allow-Origin' : '*'
            #,'Access-Control-Allow-Credentials' : 'true'
        },
        'body': json.dumps('Hello from Lambda!')
        #'body' : json.dumps(ans)
    }