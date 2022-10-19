from custom_encoder import CustomEncoder
import boto3
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

GetMethod = 'GET'
HealthPath = '/api_health'

def handler(event,context):
    client = boto3.resource('dynamodb')
    table= client.Table('user_data')
    
    logger.info(event)
    httpMethod = event['httpMethod']
    path = event['path']
    
    if httpMethod == GetMethod and path == HealthPath:
        response = buildResponse(200)
    else :
        response = buildResponse(404, 'Not Found')
        
    return response
        
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
        
        