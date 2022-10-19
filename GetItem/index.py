import json
import boto3
import logging
from custom_encoder import CustomEncoder

logger = logging.getLogger()
logger.setLevel(logging.INFO)    

GetMethod = 'GET'
GetPath= '/data_get'

def handler(event,context):
    
    logger.info(event)
    httpMethod = event['httpMethod']
    path = event['path']
    
    if httpMethod == GetMethod and path == GetPath:
        response = GetName(event['queryStringParameters']['Name'])
        
    else :
        response = buildResponse(404, 'NotFound')
        
    return response
    
    
def GetName(Name):
    
    client = boto3.resource('dynamodb')
    table= client.Table('user_data')
    
    try:
        
        response = table.get_item(
            Key={
                'Name': Name
                }
        )
        
        if 'Item' in response:
            return buildResponse(200, response['Item'])
        else :
            return buildResponse(404, {'Message':'Name : %s not found' % Name})
    
    except :
        logger.exception('TIP: Try Inserting Name into Table first')
        
    
def buildResponse(statusCode, body=None):
    response={
    'statusCode' : statusCode,
    'headers':{
         'Content-Type ': 'application/json',
         'Access-Control-Allow-Origin': '*'
         
    }    
    }
    
    if body is not None:
        response['body'] = json.dumps(body, cls=CustomEncoder)
        
    return response